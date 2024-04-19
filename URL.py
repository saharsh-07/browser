import socket
import ssl

class URL:
  def __init__(self, url):
    """
    All below code does is URI resolution.
    parts URI into protocol(scheme), host, port, path, etc
    """
    self.scheme, url = url.split("://", 1)
    assert self.scheme in ["http", "https"]
    
    if "/" not in url:
      url = url + "/"   # for handling path
    
    self.host, url = url.split("/", 1)
    self.path = "/" + url
    
    if self.scheme == "http":
      self.port = 80
    elif self.scheme == "https":
      self.port = 443
    
    if ":" in url:
      self.host, self.port = self.host.split(":", 1)
      self.port = int(port)

  # get web content from internet 
  def request(self):
    # AF - address family(various communication ways eg. internet , bluetooth, etc)
    # type - type of communication protocol (like stream, datagram , raw, etc)
    # protocol like TCP, UDP, etc.
    s = socket.socket(family = socket.AF_INET, 
               type = socket.SOCK_STREAM,
               proto = socket.IPPROTO_TCP)
    s.connect((self.host, self.port))
    
    if self.scheme == "https":  # creation of https connection is diff than http
      ctx = ssl.create_default_context()  # secure socket
      s = ctx.wrap_socket(s, server_hostname=self.host)

    req = "GET {} HTTP/1.0\r\n".format(self.path)
    req += "Host: {}\r\n".format(self.host)
    req += "\r\n"
    
    s.send(req.encode("utf-8"))
    res = s.makefile("r", encoding="utf-8", newline="\r\n")
    status_line = res.readline()
    version, status, explanation = status_line.split(" ", 2)
    
    res_headers = {}
    while True:
      line = res.readline()
    
      if line == "\r\n":
        break
    
      header, value = line.split(":", 1)
      res_headers[header.casefold()] = value.strip()
    
    assert "transfer-encoding" not in res_headers
    assert "content-encoding" not in res_headers
    
    content = res.read()
    s.close()

    return content

# text processing 
def lex(body):
  text = ""
  in_tag = False
  for c in body:
    if c == "<":
      in_tag = True
    elif c == ">":
      in_tag = False
    elif not in_tag:
      text += c
  return text

# loading of content from web 
def load(url):
  body = url.request()
  lex(body)
  
  
if __name__ == "__main__":
  import sys
  load(URL(sys.argv[1]))