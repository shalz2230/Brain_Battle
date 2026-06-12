package com.simats.brainbattle

import android.os.Bundle
import android.view.View
import android.view.ViewGroup
import android.widget.*
import androidx.appcompat.app.AppCompatActivity

class RankActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_rank)

        val listView = findViewById<ListView>(R.id.rankList)

        val users = listOf(
            Triple(1, "User1", 120),
            Triple(2, "User2", 100),
            Triple(3, "You", 90)
        )

        listView.adapter = object : ArrayAdapter<Triple<Int, String, Int>>(
            this,
            R.layout.leaderboard_item,
            users
        ) {

            override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {

                val view = layoutInflater.inflate(R.layout.leaderboard_item, parent, false)

                val rank = view.findViewById<TextView>(R.id.txtRank)
                val name = view.findViewById<TextView>(R.id.txtUser)
                val score = view.findViewById<TextView>(R.id.txtScore)

                val item = users[position]

                rank.text = item.first.toString()
                name.text = item.second
                score.text = "${item.third} ⭐"

                return view
            }
        }
    }
}