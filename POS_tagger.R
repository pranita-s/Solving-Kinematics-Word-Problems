# this function has the resposibility to generate a sense of a given text, and 
# that will be related to Wordnet dictionaey

# collect the relavant data for dictonar for yhe context
# train your model and extract the relevant pattern 
# # create dependencies trees and connect tpo wordnwet 
# # train your model with the functions AND 
# Givw the test data to verify

Semantics <- function(Sentence)
{
  library("StanfordCoreNLP")
 # source("C:/R/semantics/Wnet.R")
  
  Stanford <- StanfordCoreNLP_Pipeline()
  Stanford_parser <- StanfordCoreNLP_Pipeline("parse")
  x <- Sentence
  z_sen <- Stanford(x)
  z_sen <- as.data.frame(z_sen)
  #print(y)
  y <- Stanford_parser(x)
  
  ptexts <- sapply(subset(y, type == "sentence")$features, `[[`, "parse")
  ptexts
  depends <- lapply(subset(y, type == "sentence")$features, `[[`,
                    "basic-dependencies")
  depends <- as.data.frame(depends[[1L]])
 # print(depends)
  z <- z_sen 
  # subject identification @@@@@@@@@@@@@@@@@@@@@@@@@
  z <- as.data.frame(z)
  z <- z$features
  z <- as.data.frame(z)
  z <- z[1,]
  col_length <- ncol(z)
  i <- 2
  noun_list <- NULL
  while(i<=col_length)
  {
    if(z[1,i]=="NN")
    {
      noun_list <- c(noun_list,as.character(z[1,i+1]))
    }
    i <- i + 2
  }
  noun_list <- as.list(noun_list)
  print(noun_list)
    #print(z)
   ###############################################
  # subject tree #################################
  depends_tree <- depends
  depends_tree$POS <- NA
  i <- 1
  z_sen$id <- z_sen$id - 1
  z_sen <- z_sen[2:nrow(z_sen),]
  while(i <= (nrow(z_sen)))
  {
    for(j in 1:nrow(depends_tree))
    {
      if((depends_tree$did[j]) == (z_sen$id[i]))
      {
        depends_tree$POS[j] <- as.character(z[1,2*i]) 
      }
    }
    i <- i + 1
  }
#  print(z)
#  print(depends_tree)
  # DEPENDS Table is for refer 
#  print(depends_tree)
  
# who ########################################
  # ASSUMPTION IS 'WHO' WILL ALWAYS REFER TO NOUN
    # 1 : INITIATED FOR VERBS
  Verb_list <- NULL
  for(i in 1:nrow(depends_tree))
  {
    if(depends_tree$POS[i] == "VB" || depends_tree$POS[i] == "VBZ" || depends_tree$POS[i] == "VBG")
    {
      Verb_list <- c(Verb_list,depends_tree$dependent[i])    
    }
  }
        # GOING UP RULE TO FIND NOUN
  
  print(Verb_list)    
  
  # subject : , who , nn , 
  # adjective : what(color), this is directly assiciated with noun, 
# verb : what(subject) , 
  # direction e.g right , upon , into 
# context 
  #  what
  #  where 
  #  why
  return(depends_tree)
}
