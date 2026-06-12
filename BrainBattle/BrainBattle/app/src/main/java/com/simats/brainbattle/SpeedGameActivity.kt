package com.simats.brainbattle

import android.animation.ObjectAnimator
import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.os.CountDownTimer
import android.view.Gravity
import android.view.animation.OvershootInterpolator
import android.widget.GridLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class SpeedGameActivity : AppCompatActivity() {

    private lateinit var levelText: TextView
    private lateinit var timerText: TextView
    private lateinit var grid: GridLayout

    private var level = 1

    private var current = 1
    private var maxNumber = 6

    private var countDownTimer: CountDownTimer? = null
    private var timeLeft = 10


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_speed_game)

        levelText = findViewById(R.id.levelText)
        timerText = findViewById(R.id.timerText)
        grid = findViewById(R.id.optionsGrid)

        level = intent.getIntExtra("LEVEL", 1)

        levelText.text = "Level $level"

        setupLevel()

        startCountdown()
    }


    // =========================
    // SETUP LEVEL
    // =========================

    private fun setupLevel() {

        grid.removeAllViews()

        maxNumber = getCountForLevel()

        grid.columnCount = getColumnCount()

        val numbers =
            (1..maxNumber).toMutableList()

        numbers.shuffle()

        current = 1

        for (num in numbers) {

            val tv = TextView(this)

            val params = GridLayout.LayoutParams()

            params.width = 0
            params.height = 180

            params.columnSpec =
                GridLayout.spec(
                    GridLayout.UNDEFINED,
                    1f
                )

            params.setMargins(10,10,10,10)

            tv.layoutParams = params

            tv.gravity = Gravity.CENTER

            tv.textSize = 20f

            tv.text = num.toString()

            tv.setBackgroundResource(
                R.drawable.box_bg
            )

            tv.setOnClickListener {

                pressAnimation(tv)

                if (num == current) {

                    correctAnimation(tv)

                    current++

                    if (current > maxNumber) {

                        finishGame(3)
                    }

                } else {

                    wrongAnimation(tv)

                    finishGame(1)
                }
            }

            grid.addView(tv)
        }
    }


    // =========================
    // ANIMATIONS
    // =========================

    private fun pressAnimation(view: TextView) {

        view.animate()
            .scaleX(0.8f)
            .scaleY(0.8f)
            .setDuration(80)
            .withEndAction {

                view.animate()
                    .scaleX(1f)
                    .scaleY(1f)
                    .setDuration(80)
                    .start()

            }.start()
    }


    private fun correctAnimation(view: TextView) {

        view.setBackgroundColor(
            Color.parseColor("#4CAF50")
        )

        view.animate()
            .rotation(360f)
            .setDuration(300)
            .start()
    }


    private fun wrongAnimation(view: TextView) {

        val shake =
            ObjectAnimator.ofFloat(
                view,
                "translationX",
                0f, 20f, -20f, 15f, -15f, 10f, -10f, 0f
            )

        shake.duration = 400
        shake.start()

        view.setBackgroundColor(
            Color.parseColor("#F44336")
        )
    }


    // =========================
    // NUMBERS PER LEVEL
    // =========================

    private fun getCountForLevel(): Int {

        var count = 4 + level

        if (count > 40) count = 40

        return count
    }


    // =========================
    // GRID SIZE
    // =========================

    private fun getColumnCount(): Int {

        return when {

            level < 5 -> 3
            level < 10 -> 4
            level < 20 -> 5
            level < 40 -> 6
            level < 70 -> 7
            else -> 8
        }
    }


    // =========================
    // TIME PER LEVEL
    // =========================

    private fun getTimeForLevel(): Int {

        return when {

            level < 5 -> 10
            level < 10 -> 9
            level < 20 -> 8
            level < 40 -> 7
            level < 70 -> 6
            level < 90 -> 5
            else -> 4
        }
    }


    // =========================
    // COUNTDOWN
    // =========================

    private fun startCountdown() {

        timeLeft = getTimeForLevel()

        timerText.text = "Time $timeLeft"

        countDownTimer?.cancel()

        countDownTimer =
            object : CountDownTimer(
                (timeLeft * 1000).toLong(),
                1000
            ) {

                override fun onTick(ms: Long) {

                    timeLeft--

                    timerText.text =
                        "Time $timeLeft"
                }

                override fun onFinish() {

                    finishGame(1)
                }

            }.start()
    }


    // =========================
    // FINISH GAME
    // =========================

    private fun finishGame(stars:Int){

        countDownTimer?.cancel()

        val intent =
            Intent(
                this,
                ResultActivity::class.java
            )

        intent.putExtra(
            "LEVEL",
            level
        )

        intent.putExtra(
            "STARS",
            stars
        )

        intent.putExtra(
            "TIME",
            getTimeForLevel() - timeLeft
        )

        intent.putExtra(
            "TYPE",
            "speed"
        )

        startActivity(intent)

        finish()
    }
}