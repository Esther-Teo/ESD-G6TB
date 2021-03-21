
-- phpMyAdmin SQL Dump
-- version 4.9.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Sep 30, 2020 at 07:07 AM
-- Server version: 5.7.26
-- PHP Version: 7.4.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `WAD2PROJ` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `WAD2PROJ`;


DROP TABLE IF EXISTS `USERS`;
CREATE TABLE IF NOT EXISTS `USERS` 
(
	email varchar(100) NOT NULL,
	last_Name varchar(255) NOT NULL,
	first_Name varchar(255) DEFAULT NULL, 
	password varchar(255) NOT NULL,
	contact_Num int(8),
	telegram varchar(20) DEFAULT NULL,
	PRIMARY KEY(email)
);


DROP TABLE IF EXISTS `BOOK_LISTING`;
CREATE TABLE IF NOT EXISTS BOOK_LISTING
(
	l_id INT(10) NOT NULL AUTO_INCREMENT,
	owner_email varchar(100) NOT NULL,
	isbn varchar(255) NOT NULL,
	book_title varchar(200) NOT NULL,
	item_desc varchar(3000),
	author varchar(255),
	availability int(1) default 1,
	additional_images INT(2),
	
	PRIMARY KEY(l_id),
	FOREIGN KEY (owner_email) REFERENCES Users(email)
);


DROP TABLE IF EXISTS `BOOK_GENRE`;
CREATE TABLE IF NOT EXISTS BOOK_GENRE
(
	l_id INT(10) NOT NULL,
	genre varchar(255) NOT NULL,
	
	PRIMARY KEY(l_id, genre),
	FOREIGN KEY (l_id) REFERENCES BOOK_LISTING(l_id)
);


DROP TABLE IF EXISTS `TRADES`;
CREATE TABLE IF NOT EXISTS TRADES
(
	first_lid INT(10) NOT NULL,
	sec_lid INT(10) NOT NULL, 
	first_email varchar(100) NOT NULL,
	sec_email varchar(100) NOT NULL,
	availability int(1) DEFAULT 1,
	PRIMARY KEY(first_lid, sec_lid, first_email, sec_email),
	FOREIGN KEY (first_lid) REFERENCES BOOK_LISTING(l_id),
	FOREIGN KEY (sec_lid) REFERENCES BOOK_LISTING(l_id),
	FOREIGN KEY (first_email) REFERENCES USERS(email),
	FOREIGN KEY (sec_email) REFERENCES USERS(email)
);




/*10 users*/

INSERT INTO USERS ( email, last_Name, first_Name, password, contact_Num, telegram ) #pdopads8
VALUES ('infinty@yahoo.com', 'Johnny', 'Sins', '5dec21f340305b973b935cef098d7c6f', '9683722','doggy123');

INSERT INTO USERS ( email, last_Name, first_Name, password, contact_Num, telegram )  #smu12345
VALUES ('jackandthebean@hotmail.com','Jason', 'Lim', '7919fce5dbfa0b6f068d7368018f2050', '9683731', 'pureBlack');

INSERT INTO USERS ( email, last_Name, first_Name, password, contact_Num, telegram )   #plxzl2Aos2
VALUES ('justinbieber@mail.com','Rooster', 'Tan', 'eeb02279ec56ece385d698571931a641', '9552731', 'machina');   

INSERT INTO USERS ( email, last_Name, first_Name, password, contact_Num, telegram )   #mlpodsaj21B
VALUES ('coffebean@hotmail.com','Jonathan', 'Lim', 'cb8c1f136b478379538acc8bc08a25a9', '9559131', 'smurocks');  

INSERT INTO USERS ( email, last_Name, first_Name, password, contact_Num, telegram )   #wdaoid82aspoOP
VALUES ('unicorn666@gmail.com','Faith', 'Lim', 'b8c9ea8a15b7030814d6a5b36ab09111', '8559131', 'joinGood');  

INSERT INTO USERS ( email, last_Name, first_Name, password, contact_Num, telegram )   #Monodsa28S
VALUES ('yomhanks@yahoo.com','Sammy', 'Geeks', '03272fb328e7e8062aa35b8e41a1d9d7', '8779111', 'poeye21');  

INSERT INTO USERS ( email, last_Name, first_Name, password, contact_Num, telegram )   #Mondraw12@
VALUES ('coffebeanoe12@hotmail.com','John', 'Ang', '49cef7005e214b6f69261e6f3a0f2056', '9511131', 'rockClimb99');  

INSERT INTO USERS ( email, last_Name, first_Name, password, contact_Num, telegram )   #0kdsldad090
VALUES ('googleplot@gmail.com', 'Tomas', 'Ong', '523c8e9e404c596ae42f2c879efd4ee4', '8591327', 'fisheye5');  

INSERT INTO USERS ( email, last_Name, first_Name, password, contact_Num, telegram )   #monopoly@912
VALUES ('linkinpakr@gmail.com','Jamus', 'Lim', '70af5d4898ac3a678005e2ae80f26d97', '8237186', 'pewdiecry');  

INSERT INTO USERS ( email, last_Name, first_Name, password, contact_Num, telegram )   #jcokey213io@
VALUES ('ofcourseweA@gmail.com','Sam', 'Wicked', '2e5de6f3ddbb8db5709b2d7581be3259', '8889135', 'soccerLival');  

#Insert Book Listings

#Romance

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author, availability, additional_images) 
VALUES ("googleplot@gmail.com", "1848454449", "Christmas Ever After", "Skylar Tempest has never understood Alec Hunter's appeal. So what if he's a world-renowned historian? He's also cynical, aloof and determined to think the worst of her. So when a twist of fate finds her spending the lead-up to Christmas with Alec and his family, she's not expecting the season to be either merry or bright.", "Karen Schaler", 1, 1);

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author, availability, additional_images) 
VALUES ("ofcourseweA@gmail.com", "9780800737405", "The Edge of Belonging", "When Ivy Rose returns to her hometown to oversee an estate sale, she soon discovers that her grandmother left behind more than trinkets and photo frames--she provided a path to the truth behind Ivy's adoption. Shocked, Ivy seeks clues to her past, but a key piece to the mystery is missing. Twenty-four years earlier, Harvey James finds an abandoned newborn who gives him a sense of human connection for the first time in his life. His desire to care for the baby runs up against the stark fact that he is homeless. When he becomes entwined with two people seeking to help him find his way, Harvey knows he must keep the baby a secret or risk losing the only person he's ever loved. In this dual-time story from debut novelist Amanda Cox, the truth--both the search for it and the desire to keep it from others--takes center stage as Ivy and Harvey grapple with love, loss, and letting go.", "Amanda Cox", 1, 0);

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author, availability, additional_images) 
VALUES ("linkinpakr@gmail.com", "0800736486","Until I Met You", "When she hears that the small town of Heritage, Michigan, is looking for a new librarian, Libby Kingsley jumps at the opportunity. Little did she know the library is barely more than a storage closet stuffed with dusty, outdated books. What the community really needs is a new building. But the only funds available are those being channeled into the new town square, and the landscape architect in charge of the project wants nothing to do with her plans.All Austin Williams wants to do is get the town square project finished so he can do right by the family business and then extricate himself from the town that reveres the brother who cost him so much. But the local media and the town's new librarian seem to be conspiring against him at every turn. Will the determined bookworm find her way into his blueprints--and possibly even his heart?Novelist Tari Faris invites you back to the small town with a big heart in this second book in the Restoring Heritage series. ", "Tari Faris",  1, 0);

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author, availability, additional_images) 
VALUES ("linkinpakr@gmail.com",'1250315050', "A Highlander is Coming to Town", "The third book in the Highland, Georgia romantic comedy series from Laura Trentham, A Highlander is Coming to Town, full of love, laughs...and highlanders! You better watch out. . . Holt Pierson is dreading Christmas. His parents absconded to Florida for the season and left him to handle the family farm which will be his one day―whether he wants it or not. Driven by duty, Holt has always followed the path expected of him. But lately, he's been questioning what he wants and where he belongs. Will assuming the responsibility of the Pierson farm make him happy or is there something―or someone―else out in the wider world calling to him? To Claire Smythe, the Scottish lead singer of a touring band, Highland, Georgia, is the perfect place to hide . . .until a very handsome and deeply curious Holt begins to ask all the questions Claire doesn't want to answer. As Holt draws Claire out from under and into the fabric of small-town life, can Claire put the past behind her and embrace the unexpected gifts of the season―including the new and lasting love?", "Laura Trentham",  1, 0);

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author, availability, additional_images) 
VALUES ("yomhanks@yahoo.com", '9781949202274', "Batter of Wits", "Hate at first sight couldn't possibly exist, right? That's what Grace Buchanan thought, before her useless car stranded her on the side of a deserted road just inside the Green Valley city limits. When Tucker Haywood—tall and handsome and full of southern charm— shows up to help, her reaction to him is the strongest thing she's ever felt in her life, and it makes no freaking sense. It doesn't make much sense to Tucker either. Not why she hates him, or why he finds her so intriguing. He knows well enough that Grace is moving to Green Valley for a fresh start, not to distract him when he's got no room for something like her in his life. The complications between them are endless, but that doesn't stop her definitely not love-at-first-sight feelings from changing into something else entirely. Grace and Tucker are about to learn the hard way that in Green Valley, hating someone has never tasted so sweet. ", "Karla Sorensen", 1, 0);

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author, availability, additional_images) 
VALUES ("yomhanks@yahoo.com", "1250250463", "Cemetery Boys", "A trans boy determined to prove his gender to his traditional Latinx family summons a ghost who refuses to leave in Aiden Thomas's paranormal YA debut Cemetery Boys, described by Entertainment Weekly as 'groundbreaking.'", "Aiden Thomas",  1, 2);

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author, availability, additional_images) 
VALUES ("yomhanks@yahoo.com", "1984805703","A Rogue of One's Own", "A lady must have money and an army of her own if she is to win a revolution - but first, she must pit her wits against the wiles of an irresistible rogue bent on wrecking her plans...and her heart.", "Evie Dunmore",  1, 0);

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author, availability, additional_images) 
VALUES ("unicorn666@gmail.com", "0593098196", "The White Coat Diaries", "Grey's Anatomy meets Scrubs in this brilliant debut novel about a young doctor's struggle to survive residency, love, and life.", "Amie Kaufman, Madi Sinha",  1, 1);


INSERT INTO BOOK_GENRE (l_id, genre) VALUES (1, "Romance");
INSERT INTO BOOK_GENRE (l_id, genre) VALUES (2, "Romance");
INSERT INTO BOOK_GENRE (l_id, genre) VALUES (3, "Romance");
INSERT INTO BOOK_GENRE (l_id, genre) VALUES (4, "Romance");
INSERT INTO BOOK_GENRE (l_id, genre) VALUES (5, "Romance");
INSERT INTO BOOK_GENRE (l_id, genre) VALUES (6, "Romance");
INSERT INTO BOOK_GENRE (l_id, genre) VALUES (7, "Romance");
INSERT INTO BOOK_GENRE (l_id, genre) VALUES (8, "Romance");

#History and Biography

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author, availability, additional_images) 
VALUES ("jackandthebean@hotmail.com", '0593136306', "Agent Sonya", "The true story behind the Cold War's most intrepid female spy.", "Ben Macintyre",  1, 0);

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author, availability, additional_images) 
VALUES ("yomhanks@yahoo.com", '1616209100', "Down Along with That Devil's Bones", "In Down Along with That Devil's Bones, journalist Connor Towne O'Neill takes a deep dive into American history, exposing the still-raging battles over monuments dedicated to one of the most notorious Confederate generals, Nathan Bedford Forrest. Through the lens of these conflicts, O'Neill examines the legacy of white supremacy in America, in a sobering and fascinating work.", "Connor Towne O'Neill",  1, 0);

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author, availability, additional_images) 
VALUES ("googleplot@gmail.com", '1948742721',"Clutter: An Untidy History", "I am sitting on the floor in my mother's house, surrounded by stuff. So begins Jennifer Howard's Clutter, an expansive assessment of our relationship to the things that share and shape our lives. Sparked by the painful two-year process of cleaning out her mother's house in the wake of a devastating physical and emotional collapse, Howard sets her own personal struggle with clutter against a meticulously researched history of just how the developed world came to drown in material goods. With sharp prose and an eye for telling detail, she connects the dots between the Industrial Revolution, the Sears & Roebuck catalog, and the Container Store, and shines unsparing light on clutter's darker connections to environmental devastation and hoarding disorder. In a confounding age when Amazon can deliver anything at the click of a mouse and decluttering guru Marie Kondo can become a reality TV star, Howard's bracing analysis has never been more timely.", "Jennifer Howard ", 1, 0);

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author, availability, additional_images) 
VALUES ("coffebean@hotmail.com", '9781910620717', "The Art of Drag", "Before RuPaul's Drag Race propelled the cultural phenomenon into the global spotlight, drag had been around for thousands of years. Immerse yourself in the rich history of drag in this lusciously illustrated guide.", "Jake Hall, Sofie Birkin, HELEN LI, Jasjyot Singh Hans", 1, 0);

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author,  availability, additional_images) 
VALUES ("infinty@yahoo.com", '1538701014', "Mad and Bad: Real Heroines of the Regency", "Discover a feminist pop history that looks beyond the Ton and Jane Austen to highlight the Regency women who succeeded on their own terms and were largely lost to history -- until now.", "Bea Koch",1, 0);

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author, availability, additional_images) 
VALUES ("infinty@yahoo.com", '1250155932', "Mill Town: Reckoning with What Remains", "A galvanizing and powerful debut, Mill Town is an American story, a human predicament, and a moral wake-up call that asks: what are we willing to tolerate and whose lives are we willing to sacrifice for our own survival?", "Kerri Arsenault", 1, 0);

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author,  availability, additional_images) 
VALUES ("justinbieber@mail.com", '1982128658', "Once I Was You", "Emmy Award–winning journalist and anchor of NPR's Latino USA, Maria Hinojosa, tells the story of immigration in America through her family's experiences and decades of reporting, painting an unflinching portrait of a country in crisis.", "María Hinojosa", 1, 0);

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author,  availability, additional_images) 
VALUES ("justinbieber@mail.com", '0812997131', "JFK", "A Pulitzer Prize-winning historian takes us as close as we have ever been to the real John F. Kennedy in the first truly definitive biography of the elusive 35th president.", "Fredrik Logevall", 1, 0);


INSERT INTO BOOK_GENRE (l_id, genre) VALUES (9, "History & Biography");
INSERT INTO BOOK_GENRE (l_id, genre) VALUES (10, "History & Biography");
INSERT INTO BOOK_GENRE (l_id, genre) VALUES (11, "History & Biography");
INSERT INTO BOOK_GENRE (l_id, genre) VALUES (12, "History & Biography");
INSERT INTO BOOK_GENRE (l_id, genre) VALUES (13, "History & Biography");
INSERT INTO BOOK_GENRE (l_id, genre) VALUES (14, "History & Biography");
INSERT INTO BOOK_GENRE (l_id, genre) VALUES (15, "History & Biography");
INSERT INTO BOOK_GENRE (l_id, genre) VALUES (16, "History & Biography");


#Horror

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author, availability, additional_images) 
VALUES ("ofcourseweA@gmail.com", '0062982656', "When No One is Watching", "The gentrification of a Brooklyn neighborhood takes on a sinister new meaning… Sydney Green is Brooklyn born and raised, but her beloved neighborhood seems to change every time she blinks. Condos are sprouting like weeds, FOR SALE signs are popping up overnight, and the neighbors she's known all her life are disappearing. To hold onto her community's past and present, Sydney channels her frustration into a walking tour and finds an unlikely and unwanted assistant in one of the new arrivals to the block—her neighbor Theo. But Sydney and Theo's deep dive into history quickly becomes a dizzying descent into paranoia and fear. Their neighbors may not have moved to the suburbs after all, and the push to revitalize the community may be more deadly than advertised. When does coincidence become conspiracy? Where do people go when gentrification pushes them out? Can Sydney and Theo trust each other—or themselves—long enough to find out before they too disappear?", "Alyssa Cole", 1, 0);

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author,  availability, additional_images) 
VALUES ("ofcourseweA@gmail.com", "0316537241", "Horrid", "From the author of You Must Not Miss comes a haunting contemporary horror novel that explores themes of mental illness, rage, and grief, twisted with spine-chilling elements of Stephen King and Agatha Christie.", "Katrina Leno", 1, 0);

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author, availability, additional_images) 
VALUES ("jackandthebean@hotmail.com", "1538718006", "The Invention of Sound", "A father's decades-long search for his missing daughter. A young woman about to engineer the perfect scream. The most dangerous secret Hollywood has ever kept. Gates Foster lost his daughter, Lucy, seventeen years ago. He's never stopped searching. Suddenly, a shocking new development provides Foster with his first major lead in over a decade, and he may finally be on the verge of discovering the awful truth. Meanwhile, Mitzi Ives has carved out a space among the Foley artists creating the immersive sounds giving Hollywood films their authenticity. Using the same secret techniques as her father before her, she's become an industry-leading expert in the sound of violence and horror, creating screams so bone-chilling, they may as well be real. Soon Foster and Ives find themselves on a collision course that threatens to expose the violence hidden beneath Hollywood's glamorous façade. A grim and disturbing reflection on the commodification of suffering and the dangerous power of art, THE INVENTION OF SOUND is Chuck Palahniuk at the peak of his literary powers—his most suspenseful, most daring, and most genre-defying work yet. ", "Chuck Palahniuk", 1, 0);

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author,  availability, additional_images) 
VALUES ("jackandthebean@hotmail.com", "152580457X", "The Orphan of Cemetery Hill", "The dead won't bother you if you don't give them permission. Boston, 1844. Tabby has a peculiar gift: she can communicate with the recently departed. It makes her special, but it also makes her dangerous. As an orphaned child, she fled with her sister, Alice, from their charlatan aunt Bellefonte, who wanted only to exploit Tabby's gift so she could profit from the recent craze for seances. Now a young woman and tragically separated from Alice, Tabby works with her adopted father, Eli, the kind caretaker of a large Boston cemetery. When a series of macabre grave robberies begins to plague the city, Tabby is ensnared in a deadly plot by the perpetrators, known only as the “Resurrection Men.” In the end, Tabby's gift will either save both her and the cemetery—or bring about her own destruction.", "Hester Fox", 1, 0);

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author,  availability, additional_images) 
VALUES ("jackandthebean@hotmail.com", "1534454292", "The Loop", "Stranger Things meets World War Z in this heart-racing conspiracy thriller as a lonely young woman teams up with a group of fellow outcasts to survive the night in a town overcome by a science experiment gone wrong. Turner Falls is a small tourist town nestled in the hills of western Oregon, the kind of town you escape to for a vacation. When an inexplicable outbreak rapidly develops, this idyllic town becomes the epicenter of an epidemic of violence as the teenaged children of several executives from the local biotech firm become ill and aggressively murderous. Suddenly the town is on edge, and Lucy and her friends must do everything it takes just to fight through the night.", "Jeremy Robert Johnson", 1, 0);

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author,  availability, additional_images) 
VALUES ("ofcourseweA@gmail.com", "1492636118","Even If We Break", "From #1 New York Times bestselling author Marieke Nijkamp comes a shocking new thriller about a group of friends tied together by a game and the deadly weekend that tears them apart. FIVE friends go to a cabin. FOUR of them are hiding secrets. THREE years of history bind them. TWO are doomed from the start. ONE person wants to end this. NO ONE IS SAFE. Are you ready to play?", "Marieke Nijkamp", 1, 0);

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author,  availability, additional_images) 
VALUES ("justinbieber@mail.com", "1250304520", "White Fox", "After their world-famous actor mother disappeared under mysterious circumstances, Manon and Thaïs left their remote Mediterranean island home—sent away by their pharma-tech tycoon father. Opposites in every way, the sisters drifted apart in their grief. Yet their mother's unfinished story still haunts them both, and they can't put to rest the possibility that she is still alive. Lured home a decade later, Manon and Thaïs discover their mother's legendary last work, long thought lost: White Fox, a screenplay filled with enigmatic metaphors. The clues in this dark fairytale draw them deep into the island's surreal society, into the twisted secrets hidden by their glittering family, to reveal the truth about their mother—and themselves.", "Sara Faring",  1, 0);

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author,  availability, additional_images) 
VALUES ("justinbieber@mail.com", "0316497835", "None Shall Sleep", "The Silence of the Lambs meets Sadie in this riveting psychological thriller about two teenagers teaming up with the FBI to track down juvenile serial killers. In 1982, two teenagers—serial killer survivor Emma Lewis and US Marshal candidate Travis Bell—are recruited by the FBI to interview convicted juvenile killers and provide insight and advice on cold cases. From the start, Emma and Travis develop a quick friendship, gaining information from juvenile murderers that even the FBI can't crack. But when the team is called in to give advice on an active case—a serial killer who exclusively hunts teenagers—things begin to unravel. Working against the clock, they must turn to one of the country's most notorious incarcerated murderers for help: teenage sociopath Simon Gutmunsson. Despite Travis's objections, Emma becomes the conduit between Simon and the FBI team. But while Simon seems to be giving them the information they need to save lives, he's an expert manipulator playing a very long game...and he has his sights set on Emma. Captivating, harrowing, and chilling, None Shall Sleep is an all-too-timely exploration of not only the monsters that live among us, but also the monsters that live inside us.", "Ellie Marney",  1, 0);


INSERT INTO BOOK_GENRE (l_id, genre) VALUES (17, "Horror");
INSERT INTO BOOK_GENRE (l_id, genre) VALUES (18, "Horror");
INSERT INTO BOOK_GENRE (l_id, genre) VALUES (19, "Horror");
INSERT INTO BOOK_GENRE (l_id, genre) VALUES (20, "Horror");
INSERT INTO BOOK_GENRE (l_id, genre) VALUES (21, "Horror");
INSERT INTO BOOK_GENRE (l_id, genre) VALUES (22, "Horror");
INSERT INTO BOOK_GENRE (l_id, genre) VALUES (23, "Horror");
INSERT INTO BOOK_GENRE (l_id, genre) VALUES (24, "Horror");


#Business

INSERT INTO BOOK_LISTING (owner_email,isbn,book_title,item_desc,author, availability, additional_images) 
VALUES ("justinbieber@mail.com", "0316478520", "Talking to Strangers", "Malcolm Gladwell, host of the podcast Revisionist History and author of the #1 New York Times bestseller Outliers, offers a powerful examination of our interactions with strangers -- and why they often go wrong. How did Fidel Castro fool the CIA for a generation? Why did Neville Chamberlain think he could trust Adolf Hitler? Why are campus sexual assaults on the rise? Do television sitcoms teach us something about the way we relate to each other that isn't true? While tackling these questions, Malcolm Gladwell was not solely writing a book for the page. He was also producing for the ear. In the audiobook version of Talking to Strangers, you'll hear the voices of people he interviewed--scientists, criminologists, military psychologists. Court transcripts are brought to life with re-enactments. You actually hear the contentious arrest of Sandra Bland by the side of the road in Texas. As Gladwell revisits the deceptions of Bernie Madoff, the trial of Amanda Knox, and the suicide of Sylvia Plath, you hear directly from many of the players in these real-life tragedies. There's even a theme song - Janelle Monae's 'Hell You Talmbout.' Something is very wrong, Gladwell argues, with the tools and strategies we use to make sense of people we don't know. And because we don't know how to talk to strangers, we are inviting conflict and misunderstanding in ways that have a profound effect on our lives and our world.", "Malcolm Gladwell", 1, 0);


INSERT INTO BOOK_GENRE (l_id, genre) VALUES (25, "Business");


#Trade 
INSERT INTO TRADES(first_lid, sec_lid, first_email, sec_email, availability)
VALUES(11, 12, "googleplot@gmail.com", "ofcourseweA@gmail.com", 1 );

INSERT INTO TRADES(first_lid, sec_lid, first_email, sec_email, availability)
VALUES(16, 17, "justinbieber@mail.com", "ofcourseweA@gmail.com", 1 );

INSERT INTO TRADES(first_lid, sec_lid, first_email, sec_email, availability)
VALUES(23, 22, "justinbieber@mail.com", "ofcourseweA@gmail.com", 1 );


