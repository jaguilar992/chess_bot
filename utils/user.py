def create_user(user,first_name,last_name):
	file="./user/"+str(user)
	user_file=open(file,"w")
	user_file.write("first_name: "+first_name+"\n")
	user_file.write("last_name: "+last_name+"\n")
	user_file.close()
	return True

def get_user_info(user):
	file="./user/"+str(user)
	file=open(file,"r")
	info={}
	lines1=file.readlines()
	for line in lines1:
		if len(line)!=1:
			line=line.split("\n")[0].split(": ")
			if line[0]!="fen":
				info[line[0]]=str(line[1]).replace(" ","")
			else:
				info[line[0]]=str(line[1])
	file.close()
	return info
