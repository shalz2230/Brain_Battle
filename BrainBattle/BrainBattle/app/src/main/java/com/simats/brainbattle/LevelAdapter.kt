package com.simats.brainbattle

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

class LevelAdapter(
    private val totalLevels: Int,
    private val unlockedLevels: Int,
    private val onClick: (Int) -> Unit
) : RecyclerView.Adapter<LevelAdapter.ViewHolder>() {

    inner class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val levelNumber: TextView = view.findViewById(R.id.levelNumber)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_level, parent, false)
        return ViewHolder(view)
    }

    override fun getItemCount() = totalLevels

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val level = position + 1
        holder.levelNumber.text = level.toString()

        if (level <= unlockedLevels) {
            holder.itemView.alpha = 1f
            holder.itemView.setOnClickListener { onClick(level) }
        } else {
            holder.itemView.alpha = 0.4f
            holder.itemView.setOnClickListener(null)
        }
    }
}