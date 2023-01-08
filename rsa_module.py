import rsa


def generate_public_private_rsa_keys():
    public_key, private_key = rsa.newkeys(512)
    return {"public": public_key, "private": private_key}


def read_server_public_key():
    with open("public.pem", "rb") as f:
        return rsa.PublicKey.load_pkcs1(f.read())


def read_server_private_key():
    with open("private.pem", "rb") as f:
        return rsa.PrivateKey.load_pkcs1(f.read())

# one time executable
# must be executed first(uncomment and run this file, then comment it again)

# public_key, private_key = rsa.newkeys(2048)
#
# # Saving public key to file
# with open("public.pem", "wb") as f:
#     f.write(public_key.save_pkcs1("PEM"))
#
# # Saving private key to file
# with open("private.pem", "wb") as f:
#     f.write(private_key.save_pkcs1("PEM"))
