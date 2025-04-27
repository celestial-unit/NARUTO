package com.naruto.scoop.controllers;

import com.naruto.scoop.entities.Battle;
import com.naruto.scoop.services.BattleService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/battles")
@RequiredArgsConstructor
public class BattleController {

    private final BattleService battleService;

    @GetMapping
    public List<Battle> getAllBattles() {
        return battleService.getAllBattles();
    }

    @PostMapping
    public Battle createBattle(@RequestBody Battle battle) {
        return battleService.saveBattle(battle);
    }

    @GetMapping("/{id}")
    public Optional<Battle> getBattleById(@PathVariable Long id) {
        return battleService.getBattleById(id);
    }
}
