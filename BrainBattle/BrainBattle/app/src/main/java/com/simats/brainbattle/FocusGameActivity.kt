package com.simats.brainbattle

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.widget.ImageView
import android.widget.RelativeLayout
import androidx.appcompat.app.AppCompatActivity
import kotlin.random.Random

class FocusGameActivity : AppCompatActivity() {

    private lateinit var target: ImageView

    private val handler = Handler()

    private var level = 1
    private var time = 0


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_focus_game)

        target = findViewById(R.id.target)

        level = intent.getIntExtra("LEVEL", 1)

        startTimer()

        moveTarget()

        target.setOnClickListener {

            // ✅ player hit target
            finishGame(3)
        }
    }


    // ✅ MOVE TARGET WITH SPEED BY LEVEL
    private fun moveTarget() {

        val delay = getSpeed()

        handler.postDelayed({

            val parent =
                target.parent as RelativeLayout

            val maxX =
                parent.width - target.width

            val maxY =
                parent.height - target.height

            if (maxX <= 0 || maxY <= 0) {
                moveTarget()
                return@postDelayed
            }

            val x =
                Random.nextInt(maxX)

            val y =
                Random.nextInt(maxY)

            target.x = x.toFloat()
            target.y = y.toFloat()

            moveTarget()

        }, delay.toLong())
    }


    // ✅ SPEED BASED ON LEVEL
    private fun getSpeed(): Int {

        return when {

            level < 5 -> 800
            level < 10 -> 600
            level < 20 -> 450
            level < 40 -> 300
            level < 70 -> 200
            else -> 120
        }
    }


    // ✅ TIMER
    private fun startTimer() {

        handler.postDelayed(object : Runnable {

            override fun run() {

                time++

                handler.postDelayed(this, 1000)
            }

        }, 1000)
    }


    // ✅ FINISH GAME → RESULT SCREEN → SAVE PROGRESS
    private fun finishGame(stars: Int) {

        val intent =
            Intent(
                this,
                ResultActivity::class.java
            )

        intent.putExtra("LEVEL", level)
        intent.putExtra("STARS", stars)
        intent.putExtra("TIME", time)

        intent.putExtra("TYPE", "focus")

        startActivity(intent)

        finish()
    }
}