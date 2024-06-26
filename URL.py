import socket
import ssl
from GLOBALS import *

class URL:
  def __init__(self, url):
    """
    All below code does is URI resolution.
    parts URI into protocol(scheme), host, port, path, etc
    """
    try:
            self.scheme, url = url.split("://", 1)
            assert self.scheme in ["http", "https"]

            if "/" not in url:
                url = url + "/"
            self.host, url = url.split("/", 1)
            self.path = "/" + url

            if self.scheme == "http":
                self.port = 80
            elif self.scheme == "https":
                self.port = 443

            if ":" in self.host:
                self.host, port = self.host.split(":", 1)
                self.port = int(port)
    except:
            print("Malformed URL found, falling back to the WBE home page.")
            print("  URL was: " + url)
            self.__init__("https://browser.engineering")

  # get web content from internet 
  def request(self, top_level_url, payload=None):
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
    method = "POST" if payload else "GET"
    req = "{} {} HTTP/1.0\r\n".format(method, self.path)
    if payload:
            length = len(payload.encode("utf8"))
            req += "Content-Length: {}\r\n".format(length)
    
    req += "Host: {}\r\n".format(self.host)
    req += "\r\n"
    if self.host in COOKIE_JAR:
            cookie, params = COOKIE_JAR[self.host]
            allow_cookie = True
            if referrer and params.get("samesite", "none") == "lax":
                if method != "GET":
                    allow_cookie = self.host == referrer.host
            if allow_cookie:
                req += "Cookie: {}\r\n".format(cookie)
    if payload: req += payload
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

    return res_headers, content
  
  def origin(self):
        return self.scheme + "://" + self.host + ":" + str(self.port)

  def resolve(self, url):
        if "://" in url: return URL(url)
        if not url.startswith("/"):
            dir, _ = self.path.rsplit("/", 1)
            while url.startswith("../"):
                _, url = url.split("/", 1)
                if "/" in dir:
                    dir, _ = dir.rsplit("/", 1)
            url = dir + "/" + url
        if url.startswith("//"):
            return URL(self.scheme + ":" + url)
        else:
            return URL(self.scheme + "://" + self.host + \
                       ":" + str(self.port) + url)
  def __str__(self):
        port_part = ":" + str(self.port)
        if self.scheme == "https" and self.port == 443:
            port_part = ""
        if self.scheme == "http" and self.port == 80:
            port_part = ""
        return self.scheme + "://" + self.host + port_part + self.path
                       
# loading of content from web 
def load(url):
  nodes = HTMLParser(body).parse()
  body = URL(sys.argv[1]).request()
  print_tree(nodes)
  


