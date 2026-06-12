package com.simats.brainbattle

import android.content.Intent
import android.os.Bundle
import android.widget.LinearLayout
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.bottomnavigation.BottomNavigationView

class LevelsActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_levels)

        // Game cards
        findViewById<LinearLayout>(R.id.memory_card).setOnClickListener {
            startActivity(Intent(this, MemoryLevelsActivity::class.java))
        }

        findViewById<LinearLayout>(R.id.logic_card).setOnClickListener {
            startActivity(Intent(this, LogicLevelsActivity::class.java))
        }

        findViewById<LinearLayout>(R.id.focus_card).setOnClickListener {
            startActivity(Intent(this, FocusLevelsActivity::class.java))
        }

        findViewById<LinearLayout>(R.id.speed_card).setOnClickListener {
            startActivity(Intent(this, SpeedLevelsActivity::class.java))
        }

        // Bottom Nav
        val bottomNav = findViewById<BottomNavigationView>(R.id.bottomNav)
        bottomNav.selectedItemId = R.id.nav_levels

        bottomNav.setOnItemSelectedListener {
            when (it.itemId) {
                R.id.nav_home -> {
                    startActivity(Intent(this, HomeActivity::class.java))
                    true
                }
                R.id.nav_levels -> true
                R.id.nav_rank -> {
                    startActivity(Intent(this, RankActivity::class.java))
                    true
                }
                R.id.nav_profile -> {
                    startActivity(Intent(this, ProfileActivity::class.java))
                    true
                }
                else -> false
            }
        }
    }
}