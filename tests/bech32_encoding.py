####### Findings from encoding/decoding into bech32 #######

# Create a list with the decimal representation of a string
# This is list is based on 8 bits
data = list("https".encode("utf8"))

# Convert from 8 bits to 5 bits with
import bech32

data = bech32.convertbits(data, 8, 5)

# Use bech32_encode to encode the data into a bech32 address
bech32.bech32_encode("lnurl", data)

# To decode a you need to convert back from 5 to 8 bits
data = bech32.convertbits(data, 5, 8)

# then create a string with the representation of the 8 bits
"".join(map(chr, data))
