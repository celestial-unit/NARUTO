package com.naruto.scoop.repositories;

import com.naruto.scoop.entities.Mission;
import org.springframework.data.jpa.repository.JpaRepository;

public interface MissionRepository extends JpaRepository<Mission, Long> {
}
