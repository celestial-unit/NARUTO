package com.naruto.scoop.controllers;

import com.naruto.scoop.dto.AuthResponse;
import com.naruto.scoop.entities.User;
import com.naruto.scoop.services.JwtService;
import com.naruto.scoop.services.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final UserService userService;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

    @PostMapping("/signup")
    public User signup(@RequestBody User signupRequest) {
        signupRequest.setPassword(passwordEncoder.encode(signupRequest.getPassword()));
        signupRequest.setXp(0); // Start with 0 XP
        signupRequest.setNinjaRank("Genin"); // Default starting rank
        return userService.saveUser(signupRequest);
    }

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@RequestBody User loginRequest) {
        Optional<User> optionalUser = userService.findByUsername(loginRequest.getUsername());
        if (optionalUser.isPresent()) {
            User user = optionalUser.get();
            if (passwordEncoder.matches(loginRequest.getPassword(), user.getPassword())) {
                Map<String, Object> claims = new HashMap<>();
                claims.put("role", user.getRole());

                String jwtToken = jwtService.generateToken(claims, user.getUsername());

                return ResponseEntity.ok(new AuthResponse("Login successful", jwtToken));
            } else {
                return ResponseEntity.status(401).body(new AuthResponse("Invalid password", null));
            }
        } else {
            return ResponseEntity.status(404).body(new AuthResponse("User not found", null));
        }
    }

    @PreAuthorize("hasRole('HOKAGE')")
    @GetMapping("/promote")
    public String promoteUser() {
        var auth = SecurityContextHolder.getContext().getAuthentication();
        System.out.println("Authorities at /promote: " + auth.getAuthorities());
        return "You are authorized to promote other ninjas!";
    }


}
