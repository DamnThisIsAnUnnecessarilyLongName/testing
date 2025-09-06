import streamlit as st
from treys import Card, Deck, Evaluator
import random

from collections import Counter

def freq_suitList(text):

    lowercase_chars = [char for char in text if char.islower()]
    
    if not lowercase_chars:
        return ['d','s']
    
    counter = Counter(lowercase_chars)
    # Extract just the characters from most_common()
    return [char for char, count in counter.most_common()]


def replace_two_chars_at_index(original_string, start_index, new_chars):
    """
    Replaces two characters in a string at a specified starting index.

    Args:
        original_string (str): The string to modify.
        start_index (int): The starting index where the replacement should occur.
        new_chars (str): The two characters to insert.

    Returns:
        str: The new string with the characters replaced.
    """
    if not (0 <= start_index < len(original_string) - 1):
        raise IndexError("Start index out of bounds for replacing two characters.")
    if len(new_chars) != 2:
        raise ValueError("new_chars must contain exactly two characters.")

    return original_string[:start_index] + new_chars + original_string[start_index + 2:]

def calculate_win_probability(hole_cards, num_opponents, community_cards, num_simulations=10000, opponent_cards=None):
    """
    Calculate the probability of winning a Texas Hold'em hand.
    
    Args:
        hole_cards (str): Your hole cards in format like "AsJd" 
        num_opponents (int): Number of opponents (1-9)
        community_cards (str): Community cards like "7d2d9c" (0-5 cards)
        num_simulations (int): Number of Monte Carlo simulations to run
        opponent_cards (list): Optional list of opponent hole cards like ["KsQd", "JhTc"]
                              If None or incomplete, remaining opponents get random cards
    
    Returns:
        float: Probability of winning (0.0 to 1.0)
    """
    
    # Parse hole cards
    my_hand = []
    for i in range(0, len(hole_cards), 2):
        card_str = hole_cards[i:i+2]
        my_hand.append(Card.new(card_str))
    
    # Parse community cards
    board = []
    if community_cards:
        for i in range(0, len(community_cards), 2):
            card_str = community_cards[i:i+2]
            board.append(Card.new(card_str))
    
    # Parse known opponent cards
    known_opponent_hands = []
    all_known_cards = my_hand + board  # Track all cards we need to remove from deck
    
    if opponent_cards:
        for opp_cards in opponent_cards:
            opp_hand = []
            for i in range(0, len(opp_cards), 2):
                card_str = opp_cards[i:i+2]
                card = Card.new(card_str)
                opp_hand.append(card)
                all_known_cards.append(card)
            known_opponent_hands.append(opp_hand)
    
    # Create evaluator
    evaluator = Evaluator()
    
    wins = 0
    ties = 0
    
    for _ in range(num_simulations):
        # Create a new deck for each simulation
        deck = Deck()
        
        # Remove all known cards from deck
        for card in all_known_cards:
            deck.cards.remove(card)
        
        # Deal remaining community cards if needed
        current_board = board.copy()
        cards_needed = 5 - len(current_board)
        if cards_needed > 0:
            current_board.extend(deck.draw(cards_needed))
        
        # Set up opponent hands
        opponent_hands = known_opponent_hands.copy()  # Start with known hands
        
        # Deal random cards for remaining opponents
        remaining_opponents = num_opponents - len(known_opponent_hands)
        for _ in range(remaining_opponents):
            opponent_hand = deck.draw(2)
            opponent_hands.append(opponent_hand)
        
        # Evaluate all hands
        my_score = evaluator.evaluate(current_board, my_hand)
        opponent_scores = []
        for opponent_hand in opponent_hands:
            opponent_scores.append(evaluator.evaluate(current_board, opponent_hand))
        
        # Check if we win (lower score is better in treys)
        best_opponent_score = min(opponent_scores)
        if my_score < best_opponent_score:
            wins += 1
        elif my_score == best_opponent_score:
            ties += 1
    
    # Return win probability (ties count as half wins)
    return (wins + ties * 0.5) / num_simulations

st.title("Poker Calculator")

## init
comm_cards = ""
my_hand = ""
with st.sidebar:
    num_of_opponents = st.selectbox(
        'Number of Opponents:',
        options=[1,2],
        index=0
    )

    comm_cards = st.text_input(
        'Community cards (e.g. AsTd9c)'
    )


    my_hand = st.text_input(
        'My Hand (e.g. QdTh)'
    )

    if num_of_opponents > 0:
        opp1_hand = st.text_input(
            'Opponent 1 Hand (e.g. QdTh)'
        )
        if num_of_opponents > 1:
            opp2_hand = st.text_input(
                'Opponent 2 Hand (e.g. Jd9h)'
            )

tab1, tab2, tab3 = st.tabs(["Equity Calculator", "Debug", 'Equity table'])
with tab1:
    'Community Cards'
    # Create columns
    f_con1, f_con2, f_con3, f_con4, f_con5, f_con6 = st.columns([1, 1, 1, 1, 1, 1])

    if len(comm_cards) < 6:
        ""
    else:
        with f_con1:
            st.image("images/" + comm_cards[0:2] + '.png', use_container_width=True)
        with f_con2:
            st.image("images/" + comm_cards[2:4] + '.png', use_container_width=True)
        with f_con3:
            st.image("images/" + comm_cards[4:6] + '.png', use_container_width=True)

    'Opponent cards'
    h_con1, h_con2, h_con3, h_con4, h_con5, h_con6, h_con7, h_con8 = st.columns([1, 1, 1, 1, 1, 1, 1, 1])
    ## Opponent cards

    # Initialize
    if num_of_opponents > 0:
        if len(opp1_hand) > 3:
            with h_con1:
                st.image("images/" + opp1_hand[0:2] + '.png', use_container_width=True)
            with h_con2:
                st.image("images/" + opp1_hand[2:4] + '.png', use_container_width=True)
        else:
            with h_con1:
                st.image("images/" + 'Bk' + '.png', use_container_width=True)
            with h_con2:
                st.image("images/" + 'Bk' + '.png', use_container_width=True)
            
        # render images if selected
        if num_of_opponents > 1:
            ## Opp 1
            with h_con4:
                st.image("images/" + 'Bk' + '.png', use_container_width=True)
            with h_con5:
                st.image("images/" + 'Bk' + '.png', use_container_width=True)
            # render images if selected
            if len(opp2_hand) > 3:
                with h_con4:
                    st.image("images/" + opp2_hand[0:2] + '.png', use_container_width=True)
                with h_con5:
                    st.image("images/" + opp2_hand[2:4] + '.png', use_container_width=True)


    ## opponent hand

    "My Cards"
    m_con1, m_con2, m_con3, m_con4, m_con5, m_con6, m_con7, m_con8 = st.columns([1, 1, 1, 1, 1, 1, 1, 1])
    if len(my_hand) < 2:
        with m_con1:
            st.image("images/" + 'Bk' + '.png', use_container_width=True)
        with m_con2:
            st.image("images/" + 'Bk' + '.png', use_container_width=True)
    else:
        with m_con1:
            st.image("images/" + my_hand[0:2] + '.png', use_container_width=True)
        with m_con2:
            st.image("images/" + my_hand[2:4] + '.png', use_container_width=True)

    if len(my_hand) > 2:
        if len(opp1_hand) < 2:
            prob = calculate_win_probability(my_hand, num_opponents=num_of_opponents, community_cards=comm_cards, opponent_cards=None)
            print(prob)
            min_pot_odds = 1/((1/prob)-1)
            st.title(f"My Equity: {prob*100:.1f}%")
            st.title(f"Max bet size: {min_pot_odds:.1f}x Pot")
        else:
            prob = calculate_win_probability(my_hand, num_opponents=num_of_opponents, community_cards=comm_cards, num_simulations=10000, opponent_cards=[opp1_hand])
            print(prob)
            min_pot_odds = 1/((1/prob)-1)
            st.title(f"My Equity: {prob*100:.1f}%")
            st.title(f"Max bet size: {min_pot_odds:.1f}x Pot")
    else:
        ""
with tab2:
    #######################################################################################
    #
    # Off suits
    #
    #######################################################################################

    st.text(freq_suitList(comm_cards)) # ['d', 's']

    #####################################################################################
    # Aces
    #####################################################################################
    cardsA = []
    eq_A = []
    xs= freq_suitList(comm_cards)
    OppList = ['AA', 'AK', 'AQ', 'AJ', 'AT', 'A9', 'A8', 'A7', 'A6', 'A5', 'A4', 'A3', 'A2']
    offsuitCombo = [['d','s'], ['d','h'], ['d','c'], ['s','h'], ['s','c'], ['h','c'], ['f','f']]
    for x in OppList:
        if (x[:1] + xs[0]) in comm_cards or (x[1:] + xs[1]) in comm_cards:
            print(x[:1] + xs[0] + x[1:] + xs[1])
            for y in offsuitCombo:
                if y[0] == 'f':
                    print('fail: invalid hole cards')
                    cardsA.append('Null')
                    break

                if (x[:1] + y[0]) not in comm_cards and (x[1:] + y[1]) not in comm_cards:
                    print(x[:1] + y[0] + x[1:] + y[1])
                    cardsA.append(x[:1] + y[0] + x[1:] + y[1])
                    print(str(y) + ' success')
                    break
                else:
                    print(str(y) + ' fail')
        else:
            cardsA.append(x[:1] + xs[0] + x[1:] + xs[1])

    for oppHand in cardsA:
        eq_A.append(int(100-calculate_win_probability(my_hand, num_opponents=1, community_cards=comm_cards, num_simulations=1000, opponent_cards=[oppHand])*100))

    st.text(cardsA)
    st.text(eq_A)

    #####################################################################################
    # Kings
    #####################################################################################
    cardsK = []
    eq_K = []
    xs= freq_suitList(comm_cards)
    OppList = ['KK', 'KQ', 'KJ', 'KT', 'K9', 'K8', 'K7', 'K6', 'K5', 'K4', 'K3', 'K2']
    offsuitCombo = [['d','s'], ['d','h'], ['d','c'], ['s','h'], ['s','c'], ['h','c'], ['f','f']]
    for x in OppList:
        if (x[:1] + xs[0]) in comm_cards or (x[1:] + xs[1]) in comm_cards:
            print(x[:1] + xs[0] + x[1:] + xs[1])
            for y in offsuitCombo:
                if y[0] == 'f':
                    print('fail: invalid hole cards')
                    cardsK.append('Null')
                    break

                if (x[:1] + y[0]) not in comm_cards and (x[1:] + y[1]) not in comm_cards:
                    print(x[:1] + y[0] + x[1:] + y[1])
                    cardsK.append(x[:1] + y[0] + x[1:] + y[1])
                    print(str(y) + ' success')
                    break
                else:
                    print(str(y) + ' fail')
        else:
            cardsK.append(x[:1] + xs[0] + x[1:] + xs[1])

    for oppHand in cardsK:
        eq_K.append(int(100-calculate_win_probability(my_hand, num_opponents=1, community_cards=comm_cards, num_simulations=1000, opponent_cards=[oppHand])*100))

    st.text(cardsK)
    st.text(eq_K)        

with tab3:
    import streamlit as st
    import pandas as pd
    st.set_page_config(layout="wide") 

    "My Cards"
    n_con1, n_con2, n_con3, n_con4, n_con5, n_con6, n_con7, n_con8 = st.columns([1, 1, 1, 1, 1, 1, 1, 1])
    if len(my_hand) < 2:
        with n_con1:
            st.image("images/" + 'Bk' + '.png', use_container_width=True)
        with n_con2:
            st.image("images/" + 'Bk' + '.png', use_container_width=True)
    else:
        with n_con1:
            st.image("images/" + my_hand[0:2] + '.png', use_container_width=True)
        with n_con2:
            st.image("images/" + my_hand[2:4] + '.png', use_container_width=True)

    st.text("Opponent Hand Equity")

    # df = pd.DataFrame({
    #     ' ': ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'],
    #     'A': eq_A,
    #     'K': eq_K,
    #     'Q': eq_Q,
    #     'J': eq_J,
    #     'T': eq_T,
    #     '9': eq_9,
    #     '8': eq_8,
    #     '7': eq_7,
    #     '6': eq_6,
    #     '5': eq_5,
    #     '4': eq_4,
    #     '3': eq_3,
    #     '2': eq_2
    # }, index=['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'])

    # def color_score(val):
    #     color = 'background-color: lightgreen' if val > 51 else ''
    #     return color

    # styled_df = df.style.map(color_score, subset=['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'])
    # st.dataframe(styled_df)
