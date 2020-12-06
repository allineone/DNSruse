from socketserver import BaseRequestHandler, ThreadingUDPServer
import socket
import dns.resolver
import struct
import sys


class Handler(BaseRequestHandler):
    def resolve_query(self, message):

        query_id, flag, query_num, ans_RR_num, auth_RR_num, addi_RR_num = struct.unpack('>HHHHHH', message[0:12])
        header_info = {"query_id": query_id, "flag": flag, "query_num": query_num,"ans_RR_num": ans_RR_num, "auth_RR_num":auth_RR_num, "addi_RR_num": addi_RR_num}
        entity = message[12:]
        body = {}
        i = 1
        domain = ""
        while True:
            if entity[i] == 0:
                break
            elif entity[i] < 32:
                domain += '.'
            else:
                domain += chr(entity[i])
            i += 1
        query_bytes = entity[0:i+1]
        (query_type, query_classify) = struct.unpack('>HH', entity[i+1:i+5])
        query_length = i+5
        body.update({"domain": domain, "queryBytes": query_bytes, "queryType": query_type,"queryClassify": query_classify, "queryLen": query_length})

        return header_info, body

    def construct_message(self, header, body, ip):
        self.code = 33155 if ip == '0.0.0.0' else 33152
        msg = struct.pack('>HHHHHH', header["query_id"], self.code, header["query_num"], 1, header["auth_RR_num"], header["addi_RR_num"])
        msg += body['queryBytes'] + struct.pack('>HH', body['queryType'], body["queryClassify"])
        res = struct.pack('>HHHLH', 49164, 1, 1, 5000, 4)
        fragment = ip.split('.')
        res += struct.pack('BBBB', int(fragment[0]), int(fragment[1]), int(fragment[2]), int(fragment[3]))
        msg += res
        return msg

    def __dns_query(self, nameserver, domain):
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [nameserver]
        if domain in self.host.blacklist:
            if (self.host.redirect_ip == None) == False:
                if len(list(self.host.redirect_ip)) < 1:
                    return "0.0.0.0"
                else:
                    self.host.log("\nrequest for {}\nblacklisted, redirecting to {}".format(domain, self.host.redirect_ip))
                    return self.host.redirect_ip
            return
        else:
            try:
                try:
                    response = self.host.cache[domain]
                    self.host.log("\nrequest for {}\nretrieved {} from cache".format(domain, response))
                    return response
                except Exception:
                    response = resolver.resolve(domain, 'A')
                    self.host.log("\nrequest for {}\nresponded with {}".format(domain, str(response[0])))
                    cache = self.host.add_cache(domain, str(response[0]))
                    self.host.log(cache)
                    return str(response[0])
            except Exception as e:
                print("EXCEPTION, ", e)
            
    def __cache_clear(self):
        self.host.cache = {}


    def handle(self):
        query, sock = self.request
        query_header, query_body = self.resolve_query(query)

        if query_body['queryType'] != 1:
            sock.sendto("Sever can't handle this query type.".encode(), self.client_address)
        else:
            ip = self.__dns_query(
                self.host.dns_addr, query_body['domain'])
            if ip is None:
                sock.sendto(query, self.client_address)
            else:
                sock.sendto(self.construct_message(query_header, query_body, ip), self.client_address)
