
-- --------------------------------------------------------

--
-- Table structure for table `mocp_job_dependency`
--

CREATE TABLE `mocp_job_dependency` (
  `id` int(11) NOT NULL,
  `system` varchar(10) NOT NULL,
  `suite` varchar(10) NOT NULL,
  `job` int(10) NOT NULL,
  `dep_system` varchar(10) NOT NULL,
  `dep_suite` varchar(10) NOT NULL,
  `dep_job` int(10) NOT NULL,
  `dep_type` varchar(1) NOT NULL,
  `met_if_not_scheduled` varchar(1) DEFAULT 'N'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
