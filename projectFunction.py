#Steps:
#
#- Get level 2 nodes to accept asynchronous packets from each level 1 node (select?)
#
#- Along with packet number, send level 1 node number in header
#
#- Have level 3 node have a timer with two counter variables that track number of 
#	packets each level 1 node sends within a one second window
#
#- Level 3 sends each Level 1 node an array of tokens[x], totalTokens, 
#	and startingPkt
#
#- Level 1 nodes collect those variables and determine which packets to send
#	until next token message is received
#
#
#
#Next packet code at each of the level 1 nodes
# this code assumes two tokens at each node
currentToken = (tokens[0] < tokens[1]) ? tokens[0] : tokens[1];
nextPacketNumber = startingPkt + currentToken;
if(currentToken == tokens[0]) tokens[0] = tokens[0] + totalTokens;
else tokens[1] = tokens[1] + totalTokens; 

# Level 3 token allocation function
# this will be getting the number of packets/second from each level 1 node
# (ex. level1_1 has 28, 2 has 31, 3 has 15, and 4 has 30)
# execute this function once per second

#this part finds the lowest packets per second of any level1 node
lowest1 = (pps1 < pps2) ? pps1 : pps2;
lowest2 = (pps3 < pps4) ? pps3 : pps4;
lowest = (lowest1 < lowest2) ? lowest1 : lowest2;

#this is where the number of tokens each level1 node gets are assigned
if(pps1 > (lowest + 5)) tokensToAllocate1 = 1;	 #if pps1 is close to lowest, give it 1 token
else tokensToAllocate1 = (pps1 + 5) < lowest;  #else give it tokens proportional to its pps compared to lowest
                                               # can hardcode to 2 if issues

if(pps2 > (lowest + 5)) tokensToAllocate2 = 1; #do the same for all nodes
else tokensToAllocate2 = (pps2 + 5) < lowest; 

if(pps3 > (lowest + 5)) tokensToAllocate3 = 1;
else tokensToAllocate3 = (pps3 + 5) < lowest; 

if(pps4 > (lowest + 5)) tokensToAllocate4 = 1;
else tokensToAllocate4 = (pps4 + 5) < lowest;

totalTokens = tokensToAllocate1 + tokensToAllocate2 + tokensToAllocate3 + tokensToAllocate4;

#this is where we assign the tokens to each node
tokenNumber = 0; #first token to assign will be 0
message1 = "" + totalTokens;	 #first part of messages will be total number of tokens
message2 = "" + totalTokens;
message3 = "" + totalTokens;
message4 = "" + totalTokens;

#these variables will keep track of how many tokens each node has been assigned
tokensAllocated1, tokensAllocated2, tokensAllocated3, tokensAllocated4 = 0;

while(tokenNumber < totalTokens) #perform until all tokens are allocated

{
	if(tokensAllocated1 < tokensToAllocate1 && tokenNumber < totalTokens)
	{
		message1 = message1 + " " + tokenNumber; #allocate token by adding token number to message
		tokenNumber = tokenNumber + 1; #increment token number
		tokensAllocated1 = tokensAllocated1 + 1; #node 1 has been assigned 1 more token
	}

	if(tokensAllocated2 < tokensToAllocate2 && tokenNumber < totalTokens)
	{
		message2 = message2 + " " + tokenNumber;
		tokenNumber = tokenNumber + 1; #increment token number
		tokensAllocated2 = tokensAllocated2 + 1;
	}

	if(tokensAllocated3 < tokensToAllocate3 && tokenNumber < totalTokens)
	{
		message3 = message3 + " " + tokenNumber;
		tokenNumber = tokenNumber + 1; #increment token number
		tokensAllocated3 = tokensAllocated3 + 1;
	}

	if(tokensAllocated4 < tokensToAllocate4 && tokenNumber < totalTokens)
	{
		message4 = message4 + " " + tokenNumber;
		tokenNumber = tokenNumber + 1; #increment token number
		tokensAllocated4 = tokensAllocated4 + 1;
	}
}

message1 = message1 + " X " + startingPkt; #message format will be "totalTokens token[..] X startingPkt"
message2 = message2 + " X " + startingPkt;
message3 = message3 + " X " + startingPkt;
message4 = message4 + " X " + startingPkt;

#send messages to each node






