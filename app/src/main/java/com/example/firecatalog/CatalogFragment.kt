package com.example.firecatalog

import android.content.Intent
import android.os.Bundle
import androidx.leanback.app.BrowseSupportFragment
import androidx.leanback.widget.ArrayObjectAdapter
import androidx.leanback.widget.HeaderItem
import androidx.leanback.widget.ListRow
import androidx.leanback.widget.ListRowPresenter
import androidx.leanback.widget.OnItemViewClickedListener
import androidx.leanback.widget.Presenter
import androidx.leanback.widget.Row
import androidx.leanback.widget.RowPresenter
import com.example.firecatalog.model.CatalogItem
import com.example.firecatalog.model.SampleCatalog

/**
 * Home screen: a Leanback grid of the catalog, grouped into one row per category.
 * This is the screen the user lands on when they open the app.
 */
class CatalogFragment : BrowseSupportFragment() {

    override fun onActivityCreated(savedInstanceState: Bundle?) {
        super.onActivityCreated(savedInstanceState)

        title = getString(R.string.browse_title)
        headersState = HEADERS_ENABLED
        isHeadersTransitionOnBackEnabled = true
        brandColor = 0xFF1565C0.toInt()

        buildRows()
        setupClickListener()
    }

    private fun buildRows() {
        val rowsAdapter = ArrayObjectAdapter(ListRowPresenter())
        val cardPresenter = CardPresenter()

        val itemsByCategory: Map<String, List<CatalogItem>> =
            SampleCatalog.load().groupBy { it.category }

        itemsByCategory.forEach { (category, items) ->
            val rowAdapter = ArrayObjectAdapter(cardPresenter)
            items.forEach { rowAdapter.add(it) }

            val header = HeaderItem(category.hashCode().toLong(), category)
            rowsAdapter.add(ListRow(header, rowAdapter))
        }

        adapter = rowsAdapter
    }

    private fun setupClickListener() {
        onItemViewClickedListener = OnItemViewClickedListener {
                _: Presenter.ViewHolder?, item: Any?, _: RowPresenter.ViewHolder?, _: Row? ->
            if (item is CatalogItem) {
                val intent = Intent(requireActivity(), DetailsActivity::class.java).apply {
                    putExtra(DetailsActivity.EXTRA_ITEM, item)
                }
                startActivity(intent)
            }
        }
    }
}
