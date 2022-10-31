import code
import random

# Constants
SUITS = ('♡', '◇', '♠', '♣')
RANKS = ('Ａ', '２', '３', '４', '５', '６', '７', '８', '９', '10', 'Ｊ', 'Ｑ', 'Ｋ')
CARD_VAL = {'２':2, '３':3, '４':4, '５':5, '６':6, '７':7, '８':8, '９':9, '10':10, 'Ｊ':10, 'Ｑ':10, 'Ｋ':10, 'Ａ':11}

print("ようこそ、ブラックジャックです。")
print("あなたは、自分のカードが２１に近づくようにカードをひくかひかないか賭けをしていただきます。")

people=int(input("何人でプレーしますか。（1～3名・数字のみ記入)"))
print("かしこまりました。")
print("ルール説明")
print("初めにプレイヤーには２枚ずつのカードが配られます。")
print("その後自分の手持ちカードの合計数をみて、２１に近づけるように次のカードをひくかひかないかの選択ができます。")
print("合計数が２１に一番近い人が勝ちで、２１を超えてしまった人はその時点で負けとなってしまいます。")
print("エースは１か１１としてカウントでき、11.12.13は10とします。")
if 1<people<3:
    name1=input("プレイヤー１さん、名前を入力してください。")
    name2=input("プレイヤー２さん、名前を入力してください。")
print("それでは始めます。")

class Card(object):
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return  self.suit + ' ' + self.rank
    

class Deck(object):
    
    def __init__(self):
        self.deck = [] 
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit,rank))
                
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        dealt_card = self.deck.pop()
        return dealt_card
    

class Hand(object):
    
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    
    def add_card(self, card):
        self.cards.append(card)
        self.value += CARD_VAL[card.rank]
        if card.rank == 'Ａ':
            self.aces += 1
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
        
def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
    
def ask_hit_or_stand(deck, hand, player_turn):
    while True:
        x = input("\nカードを引きますか？引くときは y 引かないときは n を半角で入力してください。")
        
        if x == 'y':
            hit(deck,hand)  
        elif x == 'n':
            print("ディーラーのターンです。")
            player_turn = False
            return player_turn
        else:
            print("引くときは y 引かないときは n を半角で入力してください。")
            continue
        return player_turn

def show_cards_first(player, dealer):
    print("\nディーラー:")
    print('', dealer.cards[0])  
    print(" ？？")
    print("\nプレーヤー:", *player.cards, sep='\n ')
    
def show_cards_last(player, dealer):
    print("\nディーラー:", *dealer.cards, sep='\n ')
    print("ディーラーの合計:", dealer.value)
    print("\nプレーヤー:", *player.cards, sep='\n ')
    print("プレーヤーの合計", player.value)
    
def player_busts(player, dealer, money):
    print("プレーヤーがバーストしました。")
    money.player_lose()

def player_wins(player, dealer, money):
    print("プレーヤーが勝ちました。")
    money.player_win()

def dealer_busts(player, dealer, money):
    print("ディーラーがバーストしました。")
    money.player_win()
    
def dealer_wins(player, dealer, money):
    print("ディーラーが勝ちました。")
    money.player_lose()
    
def push(player, dealer):
    print("プッシュです。")

def main():
    player_turn = True
    count_game = 0
    count_win = 0
    count_tie = 0

   

    while True:
        count_game += 1
        
        print('\nカードをシャッフルします。')
        deck = Deck()
        deck.shuffle()
        
        
        print('\nカードを配ります。')
        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())
        
        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        # カードを見せる。
        show_cards_first(player_hand, dealer_hand)
        
        print('\nプレーヤーのターンです。')
        while player_turn: 
            # プレーヤーがカードを引く。
            player_turn = ask_hit_or_stand(deck, player_hand, player_turn)
            show_cards_first(player_hand, dealer_hand)
            
            # プレーヤーがバースト。
            if player_hand.value > 21:
                player_busts(player_hand, dealer_hand)
                break
        
        # プレーヤーがバーストしなければディーラーのターン。        
        if player_hand.value <= 21:
            print('\nディーラーのターンです。')
            
            # ディーラーは21以上にならなければカードを引き続ける。
            while dealer_hand.value < 17:
                hit(deck, dealer_hand)
                
            # カードを見せる。
            show_cards_last(player_hand,dealer_hand) 
            # ディーラがバースト
            if dealer_hand.value > 21:
                dealer_busts(player_hand, dealer_hand)
                count_win += 1
            # ディーラーの勝ち
            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand, dealer_hand)
            # プレーヤーの勝ち
            elif dealer_hand.value < player_hand.value:
                player_wins(player_hand, dealer_hand)
                count_win += 1
            # 引き分け
            else:
                push(player_hand,dealer_hand)
                count_tie += 1
        
        # ゲームを続けるか？
        new_game = input("続けて勝負しますか? 続けるときは y を半角で入力してください。 ")
        if new_game == 'y':
            player_turn=True
            continue
        else:
            print("\nゲームを終了します。")
            break