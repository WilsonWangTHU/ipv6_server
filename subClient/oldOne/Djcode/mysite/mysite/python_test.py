from communicate_with_server import *
from function import *

username = 'ysleep'
password = md5('ysleep')
#result = tunnel_communicate_user_auth(username,password)
#result = tunnel_communicate_create_tunnel_A(username,password)
#result = tunnel_communicate_delete_tunnel_A(username,password,'175')
result = tunnel_communicate_create_tunnel_C(username,password,'121.194.167.60')
#result = tunnel_communicate_delete_tunnel_C(username,password,'121.194.167.60')


print result
