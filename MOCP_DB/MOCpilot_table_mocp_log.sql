
-- --------------------------------------------------------

--
-- Table structure for table `mocp_log`
--

CREATE TABLE `mocp_log` (
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `system` varchar(10) NOT NULL,
  `suite` varchar(10) NOT NULL,
  `job` int(10) NOT NULL,
  `job_id` int(11) NOT NULL,
  `action` varchar(50) NOT NULL,
  `schedule_date` date NOT NULL,
  `schedule_status` varchar(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
