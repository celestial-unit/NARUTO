package com.naruto.scoop.controllers;

import com.naruto.scoop.entities.User;
import com.naruto.scoop.services.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;


    @GetMapping("/{id}")
    public Optional<User> getUserProfile(@PathVariable Long id) {
        return userService.getUserById(id);
    }

    @PreAuthorize("hasRole('HOKAGE')")
    @GetMapping("/promote")
    public String promoteUser() {
        return "You are authorized to promote other ninjas!";
    }
}
