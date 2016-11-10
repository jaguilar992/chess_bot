# -*- coding: utf-8 -*-

import telebot 
from telebot import types 
import time
import sys
import chess
import chess.uci
from time import gmtime, strftime

import utils.chessUtils as tools
import utils.info as game
import utils.settings as settings
import utils.user as userMG
from utils.engines import ENGINES
from utils.themes import THEMES

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

TOKEN = "224161699:AAHWezXcmxHq6hBoIfn0CwwLJoULXWTVNQM"
 # Nuestro tokken del bot (el que @BotFather nos dió).
bot = telebot.TeleBot(TOKEN)

CHESS_INITS=["a","b","c","d","e","f","g","h","R","N","B","Q","K","0"]
##############################################Listener
def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            cid = m.chat.id
            user=str(m.from_user.id)
            text=m.text
            user_data="["+str(user)+"@"+str(cid)+"] "
            time_stamp="["+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"]"
            log=user_data+m.text
            #LOGS
            file=open("log.txt","a")
            print time_stamp
            print log
            file.write(time_stamp+log+"\n")
            file.close()
            #CASE TEST
            if ((text[0]!='/') and (len(text)<=10) and (text[0] in CHESS_INITS)):
                play_move(m)

            # print m

bot.set_update_listener(listener) 

############################################# #Funciones Basicas
def firs_step(cid,bot):
    #SEND BOARD AND DELETING MARKUP
    markup=types.ReplyKeyboardHide(selective=False)
    bot.send_message(cid,"Beginning game...",reply_markup=markup)
    #BOARD
    caption=tools.get_last_from_pgn(cid)
    tools.send_board_image(bot,cid,caption)

    if game.get_info(cid)['game_type']=="1":
        white_name=userMG.get_user_info(game.white(cid))['first_name']
        white_last_name=userMG.get_user_info(game.white(cid))['last_name']
        white=white_name+" "+white_last_name
        black_name=userMG.get_user_info(game.black(cid))['first_name']
        black_last_name=userMG.get_user_info(game.black(cid))['last_name']
        black=black_name+" "+black_last_name
        players="Players:\nWhite: "+white+"\nBlack: "+black
        bot.send_message(cid,players)
############################################ Comportamiento del bot


@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    exist=tools.game_exist(cid)
    if not exist:
        settings.create_settings(cid)
        game.create_info(cid)
        game.update_info(cid,theme=settings.get_settings(cid)['theme'])
        tools.create_pgn_buffer(cid)
        markup=types.ReplyKeyboardMarkup(row_width=2)
        markup.add("/play vs computer","/play vs human")
        bot.send_message(cid,"Choose par:",reply_markup=markup,disable_notification=True)
        # tools.send_board_image(bot,cid)
    else:
        bot.send_message( cid, "There's a previous game",disable_notification=True) #Text

@bot.message_handler(commands=['play'])
def command_play(m):
    cid = m.chat.id
    text=m.text
    exist=tools.game_exist(cid)
    if exist and text in ["/play vs computer","/play vs human"]:
        playing_option=text.split("/play vs")[1].replace(" ","")
        if playing_option=="computer":
            game.update_info(cid,game_type="0")
        if playing_option=="human":
            game.update_info(cid,game_type="1")
        markup=types.ReplyKeyboardMarkup(row_width=2)
        markup.add("/white","/black")
        bot.send_message(cid,"Choose color:",reply_markup=markup,disable_notification=True)

@bot.message_handler(commands=['white'])
def command_white(m):
    cid = m.chat.id
    user=str(m.from_user.id)
    first_name=str(m.from_user.first_name)
    last_name=str(m.from_user.last_name)
    userMG.create_user(user,first_name, last_name)
    text=m.text
    exist=tools.game_exist(cid)
    if exist and not game.is_ready_info(cid):
        game_type=game.get_info(cid)['game_type']
        if game_type=="0":
            uci=settings.get_settings(cid)['engine']
            game.update_info(cid,white=user,black=uci,uci_white="0")
            firs_step(cid,bot)
        elif game_type=="1":
            players=[game.white(cid),game.black(cid)]
            if not user in players:
                if players[0]=="0":
                    game.update_info(cid,white=user)
                    if game.black(cid)!="0":
                        firs_step(cid,bot)
                    else:
                        bot.send_message(cid,"Waiting for /black player...")
                else:
                    bot.send_message(cid,"This color was already chosen.\nChoose /black...",disable_notification=True)
            else:
                bot.send_message(cid,"You've already chosen color.",disable_notification=True)
        # print game.get_info(cid)

@bot.message_handler(commands=['black'])
def command_white(m):
    cid = m.chat.id
    user=str(m.from_user.id)
    first_name=str(m.from_user.first_name)
    last_name=str(m.from_user.last_name)
    userMG.create_user(user,first_name, last_name)
    text=m.text
    exist=tools.game_exist(cid)
    if exist and not game.is_ready_info(cid):
        game_type=game.get_info(cid)['game_type']
        if game_type=="0":
            uci=settings.get_settings(cid)['engine']
            game.update_info(cid,white=uci,black=user,uci_white="1",flipped="1")
            #ENGINE MAKE INITIAL MOVE
            engine_move=tools.make_engine_move(cid)
            firs_step(cid,bot)
        elif game_type=="1":
            players=[game.white(cid),game.black(cid)]
            if not user in players:
                if players[1]=="0":
                    game.update_info(cid,black=user)
                    if game.white(cid)!="0":
                        firs_step(cid,bot)
                    else:
                        bot.send_message(cid,"Waiting for /white player...")
                else:
                    bot.send_message(cid,"This color was already chosen.\nChoose: /white...",disable_notification=True)
            else:
                bot.send_message(cid,"You've already chosen color.",disable_notification=True)
        # print game.get_info(cid)

 
def play_move(m):
    # print m
    cid = m.chat.id
    user=str(m.from_user.id)
    move=m.text
    exist=tools.game_exist(cid)
    if exist and game.is_ready_info(cid):
        game_type=game.get_info(cid)['game_type']
        if game_type=="0":
            legal_moves=tools.get_legal_moves(cid)
            if move in legal_moves:
                user_move=tools.make_allowed_user_move(cid,user,move)
                if user_move!="INCORRECT_TURN":
                    engine_move=tools.make_engine_move(cid)
                    if user_move!="FINISHED" or engine_move!="FINISHED":
                        caption=tools.get_last_from_pgn(cid)
                        tools.send_board_image(bot,cid,caption)
                        if tools.finished(chess.Board(game.get_info(cid)['fen'])):
                            tools.delete_game(cid)
                            bot.send_message(cid,"End...\nType for /start a new game",disable_notification=True)
                    else:
                        tools.delete_game(cid)
                        bot.send_message(cid,"Game finished...\nType for /start a new game")
        elif game_type=="1":
            legal_moves=tools.get_legal_moves(cid)
            if move in legal_moves:
                user_move=tools.make_allowed_user_move(cid,user,move)
                if user_move!="FINISHED":
                    if user_move!="INCORRECT_TURN":
                        caption=tools.get_last_from_pgn(cid)
                        tools.send_board_image(bot,cid,caption)
                else:
                    tools.delete_game(cid)
                    bot.send_message(cid,"Game finished...\nType for /start a new game")


            

@bot.message_handler(commands=['stop'])
def command_stop(m):
    cid = m.chat.id
    user=str(m.from_user.id)
    exist=tools.game_exist(cid)
    if exist:
    	if user in [game.white(cid),game.black(cid)]:
	        tools.delete_game(cid)
        	markup=types.ReplyKeyboardHide(selective=False)
        	bot.send_message(cid,"End...\nType for /start a new game",disable_notification=True,reply_markup=markup)
    	else:
	        bot.send_message(cid,"You're not allowed to stop this game")

@bot.message_handler(commands=['about']) 
def command_about(m): 
    cid = m.chat.id
    bot.send_message( cid, "Antonio Aguilar - 2016")



@bot.message_handler(commands=['board'])
def command_board(m):
    cid = m.chat.id
    user=str(m.from_user.id)
    exist=tools.game_exist(cid)
    if exist:
        caption=tools.get_last_from_pgn(cid)
        tools.send_board_image(bot,cid,caption,silent=True)
    else:
        bot.send_message(cid,"Type for /start a new game",disable_notification=True)


@bot.message_handler(commands=['fen'])
def command_fen(m):
    cid = m.chat.id
    user=str(m.from_user.id)
    exist=tools.game_exist(cid)
    if exist:
        fen=game.get_info(cid)['fen']
        bot.send_message(cid,fen,disable_notification=True)
    else:
        bot.send_message(cid,"Type for /start a new game",disable_notification=True)

@bot.message_handler(commands=['flip'])
def command_flip(m):
    cid = m.chat.id
    user=str(m.from_user.id)
    exist=tools.game_exist(cid)
    if exist:
        flipped=game.get_info(cid)['flipped']
        if flipped=="0":
            game.update_info(cid,flipped="1")
        else:
            game.update_info(cid,flipped="0")
        caption=tools.get_last_from_pgn(cid)
        tools.send_board_image(bot,cid,caption,silent=True)
    else:
        bot.send_message(cid,"Type for /start a new game",disable_notification=True)


@bot.message_handler(commands=['theme'])
def command_theme(m):
    cid = m.chat.id
    user=str(m.from_user.id)
    text=m.text
    exist=settings.settings_exist(cid)
    if exist:
        theme=text.split("/theme")[1].replace(" ","")
        if not theme in THEMES:
            markup=types.ReplyKeyboardMarkup(row_width=2)
            for key in THEMES.keys():
                markup.add("/theme "+key)
            current=game.get_info(cid)['theme']
            bot.send_message(cid, "Choose one option:\n <b>Current: </b>"+current,reply_markup=markup,parse_mode="HTML",disable_notification=True)
                
        else:
            markup=types.ReplyKeyboardHide(selective=False)
            bot.send_message(cid,"Succesful!",reply_markup=markup,disable_notification=True)
            settings.update_settings(cid,theme=theme)
            playing=tools.game_exist(cid)
            if playing:
                game.update_info(cid,theme=theme)
                caption=tools.get_last_from_pgn(cid)
                tools.send_board_image(bot,cid,caption,silent=True)




@bot.message_handler(commands=['engine'])
def command_engine(m):
    cid = m.chat.id
    user=str(m.from_user.id)
    text=m.text
    exist=settings.settings_exist(cid)
    playing=tools.game_exist(cid)
    if exist and (not playing):
        engine=text.split("/engine")[1].replace(" ","")
        if not engine in ENGINES:
            markup=types.ReplyKeyboardMarkup(row_width=2)
            for key in ENGINES:
                markup.add("/engine "+key)
            current=settings.get_settings(cid)['engine']
            bot.send_message(cid, "Choose one option:\n <b>Current: </b>"+current,reply_markup=markup,parse_mode="HTML",disable_notification=True)
                
        else:
            markup=types.ReplyKeyboardHide(selective=False)
            bot.send_message(cid,"Succesful!",reply_markup=markup,disable_notification=True)
            settings.update_settings(cid,engine=engine)









#Keep Running
bot.polling(none_stop=True)