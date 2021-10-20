
-- --------------------------------------------------------

--
-- Table structure for table `mocp_confguration`
--

CREATE TABLE `mocp_confguration` (
  `effective` datetime NOT NULL DEFAULT current_timestamp(),
  `day_start` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
