package com.naruto.scoop.entities;

import lombok.*;
import jakarta.persistence.*;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Table(name = "users") // Safer table name
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String username;
    private String password;
    private String ninjaRank;

    @Enumerated(EnumType.STRING)
    private Role role;

    private int xp;
}
