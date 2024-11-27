def sum(a,b,c):
    return a + b + c
def printboard(xstate,zstate):
    zero = 'x' if xstate[0] else ('o' if zstate[0] else 0)
    one = 'x' if xstate[1] else ('o' if zstate[1] else 1)
    two = 'x' if xstate[2] else ('o' if zstate[2] else 2)
    three = 'x' if xstate[3] else ('o' if zstate[3] else 3)
    four = 'x' if xstate[4] else ('o' if zstate[4] else 4)
    five = 'x' if xstate[5] else ('o' if zstate[5] else 5)
    six = 'x' if xstate[6] else ('o' if zstate[6] else 6)
    seven = 'x' if xstate[7] else ('o' if zstate[7] else 7)
    eight = 'x' if xstate[8] else ('o' if zstate[8] else 8)
    
    
    print(f"{zero}| {one} | {two} ")
    print("__|___|___")
    print(f"{three} | {four} | {five} ")
    print("__|___|___")
    print(f"{six} | {seven} | {eight} ")
    
def chechkwin(xstate,zstate):
    wins=[[0,1,2],[0,3,6],[3,4,5],[6,7,8],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for win in wins:
        if(sum (xstate[win[0]] , xstate[win[1]] , xstate[win[2]]) == 3):
            return 1
        if(sum (zstate[win[0]] , zstate[win[1]] , zstate[win[2]]) == 3):
            return 0
    return -1

if __name__=="__main__":
    xstate=[0,0,0,0,0,0,0,0,0]
    zstate=[0,0,0,0,0,0,0,0,0]
    turn=1
    print("welcome to tic tac toe")
    
    while(True):
        printboard(xstate,zstate)
        if turn==1:
            print("x's chance")
            value = int(input(" please Enter a value"))
            xstate[value]=1
        else:
            print("o's chance")
            value=int(input("please enter a value"))
            zstate[value]=1
        cwin=chechkwin(xstate,zstate)
        if cwin != -1:
            print("Match over!")
            if cwin == 1:
                print("X won the game!")
            else:
                print("O won the game!")
            break  # Stop the game once a player wins
        turn = 1 - turn  # Switch turns
       
        


    
    
  