
-- --------------------------------------------------------

--
-- Table structure for table `mocp_suite`
--

CREATE TABLE `mocp_suite` (
  `id` int(11) NOT NULL,
  `short_name` varchar(10) NOT NULL,
  `long_name` varchar(30) NOT NULL,
  `system` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
