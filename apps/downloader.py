from urllib.request import urlretrieve

urlretrieve(input('URL: '), f'{input("Output Dir:")}{input("Output Name: ")}')
