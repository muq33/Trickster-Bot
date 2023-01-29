# 
# def bot(queue_start:int, route:list, **kwargs):
#     i = list(kwargs.values())[0]
#     j = list(kwargs.values())[1]
#     if queue_start > 3:
#         queue_start = 1
#     if(verify_window('Trickster.bin') == True):
#         if('LifeTO' in GetWindowText(GetForegroundWindow())):
#             if queue_start == 1:
#                 PosX = mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsx))
#                 PosY = mem.read_float(getPointerAddr(mem,module + 0x009B0250, offsetsy))
#                 global walk_action
#                 if j == 0:
#                     walk_action = walk((PosX, PosY),(route[i][0],route[i][1]), 0)
#                 else:
#                     print(walk_action[1])
#                     walk_action = walk((PosX, PosY),(route[i][0],route[i][1]), walk_action[1]) 
#                 j+=1
#                 time.sleep(0.4)
#                 
#                 if walk_action[0] == True:
#                     i += 1
#                 if(i == len(route)):
#                     print("resetou")
#                     i = 0
#                 bot(queue_start + 1,route, k=i, p=j)
# #             elif queue_start == 2:
# #                 cast_skill(j % 2)
# #                 time.sleep(2.5)
#                 bot(queue_start + 1,route, k=i, p=j)
#                 
#             elif queue_start == 3:
#                 CMana = mem.read_int(getPointerAddr(mem,module + 0x009B7484, offsetscmana))
#                 Max_Mana = mem.read_int(getPointerAddr(mem,module + 0x0088A4C4, offsetsmax_mana))
#                 print(Max_Mana, CMana)
#                 verify_mana_level(j,Max_Mana)
#                 bot(queue_start +1,route, k=i, p= j)
#             else:
#                 bot(queue_start +1,route, k=i, p= j)
#         else:
#             activate_window('LifeTO', False)
#             bot(queue_start,route, k=i, p=j)
# 
#     else:
#         print('Jogo não encontrado. Finalizando aplicação')
#         exit()
#deprecated