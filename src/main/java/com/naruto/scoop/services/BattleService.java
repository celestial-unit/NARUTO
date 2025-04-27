package com.naruto.scoop.services;

import com.naruto.scoop.entities.Battle;
import com.naruto.scoop.repositories.BattleRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class BattleService {

    private final BattleRepository battleRepository;

    public List<Battle> getAllBattles() {
        return battleRepository.findAll();
    }

    public Optional<Battle> getBattleById(Long id) {
        return battleRepository.findById(id);
    }

    public Battle saveBattle(Battle battle) {
        return battleRepository.save(battle);
    }
}
