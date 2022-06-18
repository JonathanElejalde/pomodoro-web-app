#
# TABLE STRUCTURE FOR: users
#

CREATE TABLE `users` (
  `user_id` varchar(50) NOT NULL UNIQUE,
  `email` varchar(250) NOT NULL UNIQUE,
  `password` varchar(255) NOT NULL,
  `first_name` varchar(100),
  `last_name` varchar(100),
  `birth_date` date,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


#
# TABLE STRUCTURE FOR: categories
#

CREATE TABLE `categories` (
  `category_id` INT unsigned NOT NULL AUTO_INCREMENT,
  `category_name` varchar(255) NOT NULL,
  `user_id` varchar(50) NOT NULL,
  PRIMARY KEY (`category_id`),
  FOREIGN KEY (`user_id`) REFERENCES users(`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

#
# TABLE STRUCTURE FOR: projects
#

CREATE TABLE `projects` (
  `project_id` INT unsigned NOT NULL AUTO_INCREMENT,
  `user_id` varchar(50) NOT NULL,
  `category_id` INT unsigned NOT NULL,
  `project_name` varchar(250) NOT NULL,
  `start` date,
  `end` date,
  `canceled` date DEFAULT NULL,
  PRIMARY KEY (`project_id`),
  FOREIGN KEY (`user_id`) REFERENCES users(`user_id`),
  FOREIGN KEY (`category_id`) REFERENCES categories(`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


#
# TABLE STRUCTURE FOR: pomodoros
#

CREATE TABLE `pomodoros` (
  `pomodoro_id` INT unsigned NOT NULL AUTO_INCREMENT,
  `user_id` varchar(50) NOT NULL,
  `category_id` INT unsigned NOT NULL,
  `project_id` INT unsigned NOT NULL,
  `duration` INT unsigned NOT NULL,
  `pomodoro_date` datetime NOT NULL,
  `pomodoro_satisfaction` INT unsigned,
  PRIMARY KEY (`pomodoro_id`),
  FOREIGN KEY (`user_id`) REFERENCES users(`user_id`),
  FOREIGN KEY (`category_id`) REFERENCES categories(`category_id`),
  FOREIGN KEY (`project_id`) REFERENCES projects(`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


#
# TABLE STRUCTURE FOR: recall_projects
#

CREATE TABLE `recall_projects` (
  `recall_project_id` INT unsigned NOT NULL AUTO_INCREMENT,
  `user_id` varchar(50) NOT NULL,
  `project_name` varchar(255) NOT NULL,
  PRIMARY KEY (`recall_project_id`),
  FOREIGN KEY (`user_id`) REFERENCES users(`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


#
# TABLE STRUCTURE FOR: recalls
#

CREATE TABLE `recalls` (
  `recall_id` INT unsigned NOT NULL AUTO_INCREMENT,
  `user_id` varchar(50) NOT NULL,
  `recall_project_id` INT unsigned NOT NULL,
  `recall_title` varchar(255) NOT NULL,
  `recall` text,
  PRIMARY KEY (`recall_id`),
  FOREIGN KEY (`user_id`) REFERENCES users(`user_id`),
  FOREIGN KEY (`recall_project_id`) REFERENCES recall_projects(`recall_project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

