import question

if __name__ == '__main__':
    # unittests
    quests= quest_tree()
    # test the searching method
    this_quest_list = quests.find_question([1,0,3])
    for this in this_quest_list:
        print(this)

    this_quest_list = quests.find_question()
    for this in this_quest_list:
        print(this)


    # print("try to add the question into the file")
    # quests.add_question("q3",["q3a0","q3a1"])
    # # write the new question into the csv
    # csv_util.append_csv(quests)
    print("test 2")
    quests2 = quest_tree()
    print ("find the question with a new class")
    quest_find  = getQuestion(quest_tree())
    print(quest_find.findQ([1,0,3]))

    question_add = addQ(quests2)
    question_add.add_Q("q3",["q3a0","q3a1"])
	
    print ("test 3")
    quests3 = quest_tree()
    quests3.find_question[0,0,-4]
	
    quest_n = quest_node(12, "Have you been to the quad lately?", ["yes", "no", "Maybe"])
    quest_list = quest_n.getList()
    print(quest_list)
	
