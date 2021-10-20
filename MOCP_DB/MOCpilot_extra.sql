
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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `mocp_job`
--
ALTER TABLE `mocp_job`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=102;
--
-- AUTO_INCREMENT for table `mocp_job_dependency`
--
ALTER TABLE `mocp_job_dependency`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;
--
-- AUTO_INCREMENT for table `mocp_schedule`
--
ALTER TABLE `mocp_schedule`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `mocp_schedule_job`
--
ALTER TABLE `mocp_schedule_job`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2319;
--
-- AUTO_INCREMENT for table `mocp_system`
--
ALTER TABLE `mocp_system`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;