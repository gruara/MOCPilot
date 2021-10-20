
-- --------------------------------------------------------

--
-- Table structure for table `mocp_file_dependency`
--

CREATE TABLE `mocp_file_dependency` (
  `id` int(11) NOT NULL,
  `system` varchar(10) NOT NULL,
  `suite` varchar(10) NOT NULL,
  `job` int(10) NOT NULL,
  `full_path` varchar(500) NOT NULL,
  `rule` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
