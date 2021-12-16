-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 16, 2021 at 12:06 PM
-- Server version: 10.3.31-MariaDB-0+deb10u1
-- PHP Version: 7.3.31-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `MOCpilot`
--
CREATE DATABASE IF NOT EXISTS `MOCpilot` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `MOCpilot`;

-- --------------------------------------------------------

--
-- Table structure for table `mocp_confguration`
--

CREATE TABLE `mocp_confguration` (
  `effective` datetime NOT NULL DEFAULT current_timestamp(),
  `day_start` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
  `schedule_time` time NOT NULL,
  `command_line` varchar(500) NOT NULL,
  `last_scheduled` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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

-- --------------------------------------------------------

--
-- Table structure for table `mocp_schedule`
--

CREATE TABLE `mocp_schedule` (
  `id` int(11) NOT NULL,
  `schedule_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
  `schedule_time` time NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Triggers `mocp_schedule_job`
--
DELIMITER $$
CREATE TRIGGER `mocp_last_update` BEFORE UPDATE ON `mocp_schedule_job` FOR EACH ROW SET NEW.last_update=now()
$$
DELIMITER ;

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

-- --------------------------------------------------------

--
-- Table structure for table `mocp_system`
--

CREATE TABLE `mocp_system` (
  `id` int(11) NOT NULL,
  `short_name` varchar(10) NOT NULL,
  `long_name` varchar(50) NOT NULL,
  `description` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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

--
-- Indexes for dumped tables
--

--
-- Indexes for table `mocp_file_dependency`
--
ALTER TABLE `mocp_file_dependency`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `mocp_job`
--
ALTER TABLE `mocp_job`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `JOB_Key` (`system`,`suite`,`job`);

--
-- Indexes for table `mocp_job_dependency`
--
ALTER TABLE `mocp_job_dependency`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dep_system` (`dep_system`,`dep_suite`,`dep_job`);

--
-- Indexes for table `mocp_schedule`
--
ALTER TABLE `mocp_schedule`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `mocp_schedule_job`
--
ALTER TABLE `mocp_schedule_job`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `mocp_suite`
--
ALTER TABLE `mocp_suite`
  ADD KEY `system` (`system`);

--
-- Indexes for table `mocp_system`
--
ALTER TABLE `mocp_system`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `mocp_user`
--
ALTER TABLE `mocp_user`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `token` (`token`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `token_2` (`token`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `mocp_file_dependency`
--
ALTER TABLE `mocp_file_dependency`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `mocp_job`
--
ALTER TABLE `mocp_job`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `mocp_job_dependency`
--
ALTER TABLE `mocp_job_dependency`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `mocp_schedule`
--
ALTER TABLE `mocp_schedule`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `mocp_schedule_job`
--
ALTER TABLE `mocp_schedule_job`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `mocp_system`
--
ALTER TABLE `mocp_system`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
