package com.naruto.scoop.controllers;

import com.naruto.scoop.entities.Mission;
import com.naruto.scoop.services.MissionService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/missions")
@RequiredArgsConstructor
public class MissionController {

    private final MissionService missionService;

    @GetMapping
    public List<Mission> getAllMissions() {
        return missionService.getAllMissions();
    }

    @PostMapping
    public Mission createMission(@RequestBody Mission mission) {
        return missionService.saveMission(mission);
    }

    @GetMapping("/{id}")
    public Optional<Mission> getMissionById(@PathVariable Long id) {
        return missionService.getMissionById(id);
    }
}
