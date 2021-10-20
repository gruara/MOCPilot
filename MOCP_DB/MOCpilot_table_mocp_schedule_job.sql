
-- --------------------------------------------------------

--
-- Table structure for table `mocp_schedule_job`
--

CREATE TABLE `mocp_schedule_job` (
  `id` int(11) NOT NULL,
  `system` varchar(10) NOT NULL,
  `suite` varchar(10) NOT NULL,
  `job` int(10) NOT NULL,
  `status` varchar(2) NOT NULL,
  `schedule_date` date NOT NULL,
  `schedule_time` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
