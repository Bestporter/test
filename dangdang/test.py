from ProxyMiddleware import ProxyMiddleware
if __name__ == '__main__':
    ProxyMiddleware()
    if 'http://117.88.176.229:3000' in ProxyMiddleware.proxies:
        print('yse')
    else:
        print('no')