import whois

# data = raw_input("Enter a domain: ")
# raw_input renamed in python 3
data = input("Enter a domain: ")

w = whois.whois(data)

print(w)
