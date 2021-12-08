To run the testscripts to evaluate the performances follow these steps:


for private communication:
-----------------------------------------

One one terminal run the receiver node:
python3 testPerfReceiver_prv.py [receiver_client_name] 

One another terminal run sender node:
python3 testPerfSender_prv.py [sender_client_name] [receiver_client_name]


To run multiple sender-receiver pairs, on one terminal run this:
python3 testPerfReceiver_prv.py [receiver_client1_name] & python3 testPerfReceiver_prv.py [receive_client2_name]

On another terminal run this:
python3 testPerfSender_prv.py [sender_client1_name] [receiver_client1_name] & python3 testPerfSender_prv.py [sender_client2_name] [receiver_client2_name]

Keep increasing sender-receiver pairs as needed. 

for group communication:
-----------------------------------------
One one terminal run the admin as receiver node:
python3 testPerfAdmin_prv.py [receive_client_name] [group_name]

One onother terminal run the group member as senders:
python3 testPerfSender_grp.py [sender_client_name] [group_name]

Add more members to the group as:
python3 testPerfSender_grp.py [sender_client_name] [group_name] & python3 testPerfSender_grp.py [sender_client2_name] [group_name] & python3 testPerfSender_grp.py [sender_client3_name] [group_name]
