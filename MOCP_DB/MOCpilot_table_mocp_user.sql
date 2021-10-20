
-- --------------------------------------------------------

--
-- Table structure for table `mocp_user`
--

CREATE TABLE `mocp_user` (
  `user_id` varchar(250) NOT NULL,
  `name` varchar(250) NOT NULL,
  `created_on` date NOT NULL,
  `password` varchar(250) NOT NULL,
  `token` varchar(250) NOT NULL,
  `token_expiry` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
