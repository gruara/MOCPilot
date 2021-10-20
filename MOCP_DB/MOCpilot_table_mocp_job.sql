
-- --------------------------------------------------------

--
-- Table structure for table `mocp_job`
--

CREATE TABLE `mocp_job` (
  `id` int(11) NOT NULL,
  `system` varchar(10) NOT NULL,
  `suite` varchar(10) NOT NULL,
  `job` int(10) NOT NULL,
  `description` varchar(50) NOT NULL,
  `run_on` varchar(10) NOT NULL,
  `or_run_on` varchar(10) NOT NULL,
  `or_run_on2` varchar(10) NOT NULL,
  `but_not_on` varchar(10) NOT NULL,
  `and_not_on` varchar(10) NOT NULL,
  `schedule_time` datetime NOT NULL,
  `command_line` varchar(500) NOT NULL,
  `last_scheduled` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
