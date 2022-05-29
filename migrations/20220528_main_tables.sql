#
# TABLE STRUCTURE FOR: users
#

CREATE TABLE `users` (
  `user_id` INT unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(250) NOT NULL UNIQUE,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


#
# TABLE STRUCTURE FOR: categories
#

CREATE TABLE `categories` (
  `category_id` INT unsigned NOT NULL AUTO_INCREMENT,
  `category_name` varchar(255) NOT NULL,
  `user_id` INT unsigned NOT NULL,
  PRIMARY KEY (`category_id`),
  FOREIGN KEY (`user_id`) REFERENCES users(`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

#
# TABLE STRUCTURE FOR: projects
#

CREATE TABLE `projects` (
  `project_id` INT unsigned NOT NULL AUTO_INCREMENT,
  `user_id` INT unsigned NOT NULL,
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
  `user_id` INT unsigned NOT NULL,
  `category_id` INT unsigned NOT NULL,
  `project_id` INT unsigned NOT NULL,
  `duration` INT unsigned NOT NULL,
  `pomodoro_date` datetime NOT NULL,
  `pomodoro_satisfaction` INT unsigned NOT NULL,
  PRIMARY KEY (`pomodoro_id`),
  FOREIGN KEY (`user_id`) REFERENCES users(`user_id`),
  FOREIGN KEY (`category_id`) REFERENCES categories(`category_id`),
  FOREIGN KEY (`project_id`) REFERENCES projects(`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

#
# TABLE STRUCTURE FOR: recalls
#

CREATE TABLE `recalls` (
  `recall_id` INT unsigned NOT NULL AUTO_INCREMENT,
  `user_id` INT unsigned NOT NULL,
  `project_name` varchar(255) NOT NULL,
  `recall` text,
  `recall_title` varchar(255) NOT NULL,
  PRIMARY KEY (`recall_id`),
  FOREIGN KEY (`user_id`) REFERENCES users(`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

