import qrcode
import sys
a=qrcode.QRCode(version=1,box_size=30,border=2)
w=sys.argv
print(type(w))
# e=eval(w)
# print((e))
v=a.add_data(w)
a.make(fit=True)
b=a.make_image(fill_color="black",back_color="white")

# d=list(v[0].values())
b.save("studentqr.jpg")
# print(d)