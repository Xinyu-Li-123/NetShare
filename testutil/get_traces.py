import gdown


output_traces = "/nfs/NetShare/traces"
url_traces = "https://drive.google.com/drive/folders/1FOl1VMr0tXhzKEOupxnJE9YQ2GwfX2FD?usp=share_link"
gdown.download_folder(url=url_traces, output=output_traces, quiet=False, use_cookies=False)

output_testtraces = "/nfs/NetShare/traces/testpcap"
url_testtraces = "https://drive.google.com/drive/folders/12Yvbjt98Xi6Folb-aIDlfsUtS8IdRyy5?usp=share_link"
gdown.download_folder(url=url_testtraces, output=output_testtraces, quiet=False, use_cookies=False)

