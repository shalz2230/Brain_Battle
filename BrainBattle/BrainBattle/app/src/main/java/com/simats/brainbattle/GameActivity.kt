package com.simats.brainbattle

import android.content.Intent
import android.os.Bundle
import android.os.CountDownTimer
import android.os.Handler
import android.view.Gravity
import android.widget.GridLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class GameActivity : AppCompatActivity() {

    private lateinit var grid: GridLayout
    private lateinit var timerText: TextView
    private lateinit var levelText: TextView

    private var level = 1

    private var moves = 0
    private var mistakes = 0
    private var time = 0

    private var totalCards = 16
    private var pairs = 8

    private val values = mutableListOf<Int>()

    private var firstCard: TextView? = null
    private var firstValue = -1

    private var matchedPairs = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.game_screen)

        grid = findViewById(R.id.gameGrid)
        timerText = findViewById(R.id.timerText)
        levelText = findViewById(R.id.levelText)

        level = intent.getIntExtra("LEVEL", 1)
        levelText.text = "Level $level"

        setDifficulty()
        generateCards()
        startTimer()
    }

    // ✅ Difficulty based on level
    private fun setDifficulty() {

        totalCards = when {
            level < 5 -> 16
            level < 10 -> 20
            else -> 24
        }

        pairs = totalCards / 2

        val col = Math.sqrt(totalCards.toDouble()).toInt()
        grid.columnCount = col
    }

    // ✅ Generate cards
    private fun generateCards() {

        grid.removeAllViews()
        values.clear()

        for (i in 1..pairs) {
            values.add(i)
            values.add(i)
        }

        values.shuffle()

        for (i in 0 until totalCards) {

            val tv = TextView(this)

            val params = GridLayout.LayoutParams()
            params.width = 0
            params.height = 180
            params.columnSpec =
                GridLayout.spec(
                    GridLayout.UNDEFINED,
                    1f
                )

            params.setMargins(8, 8, 8, 8)

            tv.layoutParams = params
            tv.gravity = Gravity.CENTER
            tv.textSize = 20f
            tv.setTextColor(resources.getColor(android.R.color.black))

            tv.setBackgroundResource(
                R.drawable.card_back
            )

            val value = values[i]

            tv.setOnClickListener {

                if (tv.text != "" || tv == firstCard)
                    return@setOnClickListener

                tv.text = value.toString()
                tv.setBackgroundResource(
                    R.drawable.box_bg
                )

                if (firstCard == null) {

                    firstCard = tv
                    firstValue = value

                } else {

                    moves++

                    if (firstValue == value) {

                        matchedPairs++
                        firstCard = null

                        if (matchedPairs == pairs) {
                            finishGame()
                        }

                    } else {

                        mistakes++

                        Handler().postDelayed({

                            tv.text = ""
                            tv.setBackgroundResource(
                                R.drawable.card_back
                            )

                            firstCard?.text = ""
                            firstCard?.setBackgroundResource(
                                R.drawable.card_back
                            )

                            firstCard = null

                        }, 600)
                    }
                }
            }

            grid.addView(tv)
        }
    }

    // ✅ Timer
    private fun startTimer() {

        object : CountDownTimer(
            600000,
            1000
        ) {

            override fun onTick(ms: Long) {

                time++
                timerText.text =
                    "Time $time s"
            }

            override fun onFinish() {}

        }.start()
    }

    // ✅ Finish game → calculate stars
    private fun finishGame() {

        val idealMoves = pairs
        val extraMoves = moves - idealMoves

        val stars = when {

            extraMoves <= 2 -> 3

            extraMoves <= 6 -> 2

            else -> 1
        }

        openResultScreen(stars)
    }

    // ✅ Open result screen
    private fun openResultScreen(
        stars: Int
    ) {

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
            time
        )

        startActivity(intent)
        finish()
    }
}