package com.naruto.scoop.repositories;

import com.naruto.scoop.entities.Battle;
import org.springframework.data.jpa.repository.JpaRepository;

public interface BattleRepository extends JpaRepository<Battle, Long> {
}
