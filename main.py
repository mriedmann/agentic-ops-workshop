from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


def main():
    address = ("127.0.0.1", 8000)
    print(f"Serving the workshop at http://{address[0]}:{address[1]}")
    ThreadingHTTPServer(address, SimpleHTTPRequestHandler).serve_forever()


if __name__ == "__main__":
    main()
