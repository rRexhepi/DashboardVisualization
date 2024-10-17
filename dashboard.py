import os
import pandas as pd
from bokeh.io import output_file, show
from bokeh.layouts import column, row
from bokeh.models import (
    Div,
    ColumnDataSource,
    DataTable,
    TableColumn,
    TabPanel,
    Tabs,
    Button,
    CustomJS,
    Checkbox,
    CustomJSFilter,
    CDSView,
    Select,
    AutocompleteInput,
    NumberFormatter,
    DateFormatter,
    HoverTool
)
from bokeh.themes import Theme
from bokeh.plotting import figure

# ============================
# Define Color Palette
# ============================
PRIMARY_COLOR = "#2F4F4F"      # Dark Slate Gray
SECONDARY_COLOR = "#4682B4"    # Steel Blue
BACKGROUND_COLOR = "#F5F5F5"   # White Smoke
TEXT_COLOR = "#333333"         # Dark Gray
ACCENT_COLOR = "#20B2AA"        # Light Sea Green

# ============================
# CSS and HTML Configuration
# ============================

# Header and Footer Styles
header_div_style = {
    "color": PRIMARY_COLOR,
    "text-align": "center",
    "margin": "20px 0",
    "font-family": "Arial, sans-serif"
}

footer_div_style = {
    "color": TEXT_COLOR,
    "text-align": "left",
    "margin": "20px",
    "font-family": "Arial, sans-serif",
    "font-size": "12px"
}

# JavaScript for Exporting Data
ExportDataJavaScript = """
function getcsv(source, file) {
    const columns = Object.keys(source.data);
    const nrows = source.get_length();
    const lines = [columns.join(',')];  // Use comma as delimiter for column headers

    for (let i = 0; i < nrows; i++) {
        let row = []
        for (let j = 0; j < columns.length; j++) {
            const column = columns[j]
            // Encapsulate each field in double quotes and escape existing quotes
            const value = source.data[column][i].toString().replace(/"/g, '""')
            row.push('"' + value + '"')
        }
        lines.push(row.join(','))  // Comma as delimiter for data
    }
    const filetext = lines.join('\\n').concat('\\n');
    const blob = new Blob([filetext], {type: 'text/csv; charset=utf-8;'})
    
    // Addresses IE
    if (navigator.msSaveBlob) {
        navigator.msSaveBlob(blob, file)
    } else {
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = file
        link.target = '_blank'
        link.style.visibility = 'hidden'
        link.dispatchEvent(new MouseEvent('click'))
    }
}
"""

# ============================
# Verify and Create Output Directory
# ============================

output_directory = 'data/output'
output_html_path = os.path.join(output_directory, 'Dashboard.html')

if not os.path.exists(output_directory):
    try:
        os.makedirs(output_directory)
        print(f"Created output directory at: {output_directory}")
    except Exception as e:
        print(f"Error creating output directory: {e}")
        raise
else:
    print(f"Output directory already exists at: {output_directory}")

# ============================
# Define Output HTML File
# ============================
print(f"Generating dashboard at: {output_html_path}")

# Configure the output file
output_file(output_html_path, title='Dashboard')

# ============================
# Define a Custom Theme
# ============================
custom_theme = Theme(json={
    'attrs': {
        'DataTable': {
            'headers': {
                'background': PRIMARY_COLOR,
                'foreground': 'white',
                'font': 'Arial, sans-serif',
                'font-size': '12pt'
            },
            'cells': {
                'background': 'white',
                'foreground': 'black',
                'font': 'Arial, sans-serif',
                'font-size': '11pt'
            }
        },
        'Div': {
            'text': {
                'font-family': 'Arial, sans-serif'
            }
        },
        'Button': {
            'button': {
                'background': ACCENT_COLOR,
                'color': 'white',
                'font-family': 'Arial, sans-serif',
                'border-radius': '5px',
                'padding': '8px 16px',
                'border': 'none',
                'cursor': 'pointer'
            }
        },
        'Select': {
            'select': {
                'font-family': 'Arial, sans-serif',
                'font-size': '12pt'
            }
        },
        'AutocompleteInput': {
            'autocomplete-input': {
                'font-family': 'Arial, sans-serif',
                'font-size': '12pt'
            }
        },
        'Checkbox': {
            'checkbox': {
                'font-family': 'Arial, sans-serif',
                'font-size': '12pt'
            }
        }
    }
})

# ============================
# TAB 0: Summary
# ============================

try:
    print("Loading BFIPublicDataDF...")
    # Path to the data
    output_file_path = 'data/input/tabula-bfi-payments-over-25000-report-2014-15.csv'

    # Load the data
    BFIPublicDataDF = pd.read_csv(output_file_path)
    print("BFIPublicDataDF loaded successfully:")
    print(BFIPublicDataDF.head())

    # Convert data types
    BFIPublicDataDF = BFIPublicDataDF.convert_dtypes(convert_string=True)

    # Specify the date format based on your data
    print("Parsing Dates in BFIPublicDataDF...")
    BFIPublicDataDF['Date'] = pd.to_datetime(
        BFIPublicDataDF['Date'], 
        format="%d/%m/%y",
        errors='coerce'
    )
    BFIPublicDataDF['Month'] = BFIPublicDataDF['Date'].dt.strftime('%B %Y')
    print("Month extraction complete:")
    print(BFIPublicDataDF[['Date', 'Month']].head())

    # Clean and convert 'Amount' to numeric in Summary Tab
    print("Cleaning and converting 'Amount' column to numeric in Summary Tab...")
    BFIPublicDataDF['Amount'] = BFIPublicDataDF['Amount'].replace({'£': '', ',': ''}, regex=True)
    BFIPublicDataDF['Amount'] = pd.to_numeric(BFIPublicDataDF['Amount'], errors='coerce').fillna(0.0)
    print("After cleaning, 'Amount' column in Summary Tab:")
    print(BFIPublicDataDF['Amount'].head())

    # Aggregate total records by Month
    SummaryDf = BFIPublicDataDF.groupby('Month').size().reset_index(name='Total Records')
    print("Aggregated Summary:")
    print(SummaryDf.head())

    # Configure data source
    BFIPublicDataDFSource = ColumnDataSource(SummaryDf)

    # Configure table columns
    BFIPublicDataDFColumns = [
        TableColumn(field="Month", title="Month", width=150),
        TableColumn(field="Total Records", title="Total Records", width=150, formatter=NumberFormatter(format="0,0"))
    ]

    # Configure table
    BFIPublicDataDFTable = DataTable(
        source=BFIPublicDataDFSource,
        columns=BFIPublicDataDFColumns,
        index_position=None,
        reorderable=False,
        width=500,
        height=400,
        height_policy='auto'
    )

    # Configure Divs
    BFIPublicDataDFHeaderDiv = Div(
        text="<h2>Summary of Datasets</h2>",
        styles=header_div_style,
        width=800
    )

    BFIPublicDataDFFooterDiv = Div(
        text="""
            <p><b>Data Sources:</b> Data Source is British Film Institute Spend over £25000 public dataset.</p>
            <p><b>Data:</b> Downloadable Data for the dataset</p>
            <p><b>Graphs:</b> Interactive Graphs for the dataset</p>
        """,
        styles=footer_div_style,
        width=800
    )

    # Configure layout for Tab 0
    BFIPublicDataDFGridPlot = column(
        BFIPublicDataDFHeaderDiv,
        BFIPublicDataDFTable,
        BFIPublicDataDFFooterDiv
    )
    print("BFIPublicDataDFGridPlot constructed successfully.")

    # Define TabPanel for Tab 0
    tab0 = TabPanel(child=BFIPublicDataDFGridPlot, title="Summary")

except Exception as e:
    print(f"Error processing Tab 0 data: {e}")
    raise

# ============================
# TAB 1: Data
# ============================

try:
    print("Loading BFIPublicDataDF for Data Tab...")
    # Path to the data file (CSV format)
    vouchers_data_path = 'data/input/tabula-bfi-payments-over-25000-report-2014-15.csv'

    # Load the data
    BFIPublicDataDF_DataTab = pd.read_csv(vouchers_data_path)
    BFIPublicDataDF_DataTab.fillna("", inplace=True)
    print("BFIPublicDataDF loaded successfully:")
    print(BFIPublicDataDF_DataTab.head())
    print(f"Record Count: {BFIPublicDataDF_DataTab.shape}")

    # Specify the date format based on your data
    print("Parsing Dates in BFIPublicDataDF_DataTab...")
    BFIPublicDataDF_DataTab['Date'] = pd.to_datetime(
        BFIPublicDataDF_DataTab['Date'],
        format="%d/%m/%y",  # Two-digit year
        errors='coerce'
    )
    BFIPublicDataDF_DataTab['Month'] = BFIPublicDataDF_DataTab['Date'].dt.strftime('%B %Y')
    print("Month extraction complete:")
    print(BFIPublicDataDF_DataTab[['Date', 'Month']].head())

    # Clean and convert 'Amount' to numeric
    print("Cleaning and converting 'Amount' column to numeric...")
    BFIPublicDataDF_DataTab['Amount'] = BFIPublicDataDF_DataTab['Amount'].replace({'£': '', ',': ''}, regex=True)
    BFIPublicDataDF_DataTab['Amount'] = pd.to_numeric(BFIPublicDataDF_DataTab['Amount'], errors='coerce').fillna(0.0)
    print("After cleaning, 'Amount' column:")
    print(BFIPublicDataDF_DataTab['Amount'].head())

    # Configure source
    BFIPublicDataDFSource_DataTab = ColumnDataSource(BFIPublicDataDF_DataTab)

    # Create AutocompleteInput for 'Expense Area'
    ExpenseAreaCompletions = sorted(BFIPublicDataDF_DataTab['Expense Area'].unique().tolist())

    ExpenseAreaAutocompleteInput = AutocompleteInput(
        title="Search Expense Area",
        search_strategy="includes",
        case_sensitive=False,
        restrict=False,
        placeholder='',
        completions=ExpenseAreaCompletions,
        width=300
    )

    # Dropdowns for Supplier, Month, and Transaction Ref
    SupplierSelect = Select(
        title="Supplier",
        value='All',
        options=['All'] + sorted(BFIPublicDataDF_DataTab['Supplier'].unique().tolist()),
        width=200
    )

    MonthSelect = Select(
        title="Month",
        value='All',
        options=['All'] + sorted(BFIPublicDataDF_DataTab['Month'].dropna().unique().tolist()),
        width=200
    )

    TransactionRefSelect = Select(
        title="Transaction Ref",
        value='All',
        options=['All'] + sorted(BFIPublicDataDF_DataTab['Transaction Ref'].unique().tolist()),
        width=300
    )

    # Expense Area autocomplete callback
    ExpenseAreaCallback = CustomJS(
        args=dict(
            source=BFIPublicDataDFSource_DataTab,
            expense_area_autocomplete=ExpenseAreaAutocompleteInput,
            supplier_select=SupplierSelect,
            month_select=MonthSelect,
            transaction_ref_select=TransactionRefSelect
        ),
        code="""
        const expense_area = expense_area_autocomplete.value.toLowerCase();
        const data = source.data;
        const indices = [];
        const suppliers = new Set();
        const months = new Set();
        const transactionRefs = new Set();

        for (let i = 0; i < data['Expense Area'].length; i++) {
            const expense_area_value = data['Expense Area'][i].toString().toLowerCase();
            if (expense_area === '' || expense_area_value.includes(expense_area)) {
                indices.push(i);
                suppliers.add(data['Supplier'][i].toString());
                months.add(data['Month'][i].toString());
                transactionRefs.add(data['Transaction Ref'][i].toString());
            }
        }

        // Update dropdowns based on filtered Expense Area
        supplier_select.options = ['All'].concat(Array.from(suppliers).sort());
        supplier_select.value = 'All';
        
        month_select.options = ['All'].concat(Array.from(months).sort());
        month_select.value = 'All';
        
        transaction_ref_select.options = ['All'].concat(Array.from(transactionRefs).sort());
        transaction_ref_select.value = 'All';

        // Update the data table based on Expense Area filtering
        source.selected.indices = indices;
        source.change.emit();
        """
    )
    ExpenseAreaAutocompleteInput.js_on_change('value', ExpenseAreaCallback)

    # Supplier select callback
    SupplierCallback = CustomJS(
        args=dict(
            source=BFIPublicDataDFSource_DataTab,
            supplier_select=SupplierSelect,
            month_select=MonthSelect,
            expense_area_autocomplete=ExpenseAreaAutocompleteInput,
            transaction_ref_select=TransactionRefSelect
        ),
        code="""
        const supplier = supplier_select.value;
        const data = source.data;
        const indices = [];
        const months = new Set();
        const transactionRefs = new Set();

        for (let i = 0; i < data['Supplier'].length; i++) {
            if (supplier === 'All' || data['Supplier'][i] === supplier) {
                indices.push(i);
                months.add(data['Month'][i].toString());
                transactionRefs.add(data['Transaction Ref'][i].toString());
            }
        }

        // Update dropdowns based on supplier filtering
        month_select.options = ['All'].concat(Array.from(months).sort());
        month_select.value = 'All';
        
        transaction_ref_select.options = ['All'].concat(Array.from(transactionRefs).sort());
        transaction_ref_select.value = 'All';

        source.selected.indices = indices;
        source.change.emit();
        """
    )
    SupplierSelect.js_on_change('value', SupplierCallback)

    # Month select callback
    MonthCallback = CustomJS(
        args=dict(
            source=BFIPublicDataDFSource_DataTab,
            supplier_select=SupplierSelect,
            month_select=MonthSelect,
            expense_area_autocomplete=ExpenseAreaAutocompleteInput,
            transaction_ref_select=TransactionRefSelect
        ),
        code="""
        const month = month_select.value;
        const data = source.data;
        const indices = [];
        const suppliers = new Set();
        const transactionRefs = new Set();

        for (let i = 0; i < data['Month'].length; i++) {
            if (month === 'All' || data['Month'][i] === month) {
                indices.push(i);
                suppliers.add(data['Supplier'][i].toString());
                transactionRefs.add(data['Transaction Ref'][i].toString());
            }
        }

        // Update dropdowns based on month filtering
        supplier_select.options = ['All'].concat(Array.from(suppliers).sort());
        supplier_select.value = 'All';
        
        transaction_ref_select.options = ['All'].concat(Array.from(transactionRefs).sort());
        transaction_ref_select.value = 'All';

        source.selected.indices = indices;
        source.change.emit();
        """
    )
    MonthSelect.js_on_change('value', MonthCallback)

    # Transaction Ref select callback
    TransactionRefCallback = CustomJS(
        args=dict(source=BFIPublicDataDFSource_DataTab, transaction_ref_select=TransactionRefSelect),
        code="""
        const transaction_ref = transaction_ref_select.value;
        const data = source.data;
        const indices = [];
        for (let i = 0; i < data['Transaction Ref'].length; i++) {
            if (transaction_ref === 'All' || data['Transaction Ref'][i].toString() === transaction_ref) {
                indices.push(i);
            }
        }
        source.selected.indices = indices; // Update selected indices
        source.change.emit();
        """
    )
    TransactionRefSelect.js_on_change('value', TransactionRefCallback)

    # Checkbox Filters
    checkbox_filter_paid = Checkbox(label="Paid Only", active=False)
    checkbox_filter_unpaid = Checkbox(label="Unpaid Only", active=False)

    # Filter based on multiple criteria
    BFIPublicDataDFFilter = CustomJSFilter(
        args=dict(
            supplier_select=SupplierSelect,
            month_select=MonthSelect,
            expense_area_autocomplete=ExpenseAreaAutocompleteInput,
            transaction_ref_select=TransactionRefSelect,
            checkbox_paid=checkbox_filter_paid,
            checkbox_unpaid=checkbox_filter_unpaid
        ),
        code="""
        const selectedSupplier = supplier_select.value;
        const selectedMonth = month_select.value;
        const expense_area = expense_area_autocomplete.value.toLowerCase();
        const transaction_ref = transaction_ref_select.value;
        const only_show_paid = checkbox_paid.active;
        const unpaid_only = checkbox_unpaid.active;
        const data = source.data;
        const indices = [];

        for (let i = 0; i < data['Supplier'].length; i++) {
            const amount = data['Amount'][i];
            const supplierMatch = (selectedSupplier === 'All') || (data['Supplier'][i] === selectedSupplier);
            const monthMatch = (selectedMonth === 'All') || (data['Month'][i] === selectedMonth);
            const expenseAreaMatch = (expense_area === '') || (data['Expense Area'][i].toLowerCase().includes(expense_area));
            const transactionRefMatch = (transaction_ref === 'All') || (data['Transaction Ref'][i].toString() === transaction_ref);
            const paidMatch = (!only_show_paid) || (amount > 0);
            const unpaidMatch = (!unpaid_only) || (amount === 0);

            if (supplierMatch && monthMatch && expenseAreaMatch && transactionRefMatch && paidMatch && unpaidMatch) {
                indices.push(i);
            }
        }

        return indices;
        """
    )

    # Add checkbox change callback to refresh the data source
    checkbox_callback = CustomJS(
        args=dict(source=BFIPublicDataDFSource_DataTab),
        code="""
        source.change.emit();
        """
    )
    checkbox_filter_paid.js_on_change('active', checkbox_callback)
    checkbox_filter_unpaid.js_on_change('active', checkbox_callback)

    # Configure CDS view
    BFIPublicDataDFView = CDSView(filter=BFIPublicDataDFFilter)

    # Configure table columns
    BFIPublicDataDFColumns = [
        TableColumn(field='Dept Family', title='Dept Family', width=150),
        TableColumn(field='Entity', title='Entity', width=200),
        TableColumn(field='Date', title='Date', formatter=DateFormatter(format="%d/%m/%Y"), width=150),
        TableColumn(field='Expense Area', title='Expense Area', width=150),
        TableColumn(field='Expense Type', title='Expense Type', width=150),
        TableColumn(field='Supplier', title='Supplier', width=200),
        TableColumn(field='Transaction Ref', title='Transaction Ref', width=200),
        TableColumn(field='Amount', title='Amount (£)', formatter=NumberFormatter(format='£0,0.00'), width=120)
    ]

    # Configure table
    BFIPublicDataDFTable = DataTable(
        source=BFIPublicDataDFSource_DataTab,
        columns=BFIPublicDataDFColumns,
        view=BFIPublicDataDFView,
        index_position=None,
        reorderable=False,
        width=1500,
        height=500,
        height_policy='auto'
    )

    # Configure download button
    BFIPublicDataDFDownloadButton = Button(
        label="Download",
        button_type="primary",
        width=120
    )
    BFIPublicDataDFDownloadButton.js_on_click(CustomJS(
        args=dict(file='BFIOver25000Data.csv', source=BFIPublicDataDFSource_DataTab),
        code=ExportDataJavaScript + "\n getcsv(source, file);"
    ))

    # Configure Div for Data Tab Header
    DataHeaderDiv = Div(
        text="<h2> Data </h2>",
        styles=header_div_style,
        width=1600
    )

    # Arrange Filters in a Row
    filters_row = row(
        ExpenseAreaAutocompleteInput,
        SupplierSelect,
        MonthSelect,
        TransactionRefSelect,
        sizing_mode='stretch_width',
        width=1600
    )

    # Arrange Checkboxes in a Row
    checkboxes_row = row(
        checkbox_filter_paid,
        checkbox_filter_unpaid,
        sizing_mode='stretch_width',
        width=1600
    )

    # Configure layout for Tab 1
    BFIPublicDataDFGridPlot = column(
        DataHeaderDiv,
        filters_row,
        checkboxes_row,
        BFIPublicDataDFTable,
        BFIPublicDataDFDownloadButton,
        sizing_mode='stretch_both'
    )
    print("BFIPublicGridPlot constructed successfully.")

    # Define TabPanel for Tab 1
    tab1 = TabPanel(child=BFIPublicDataDFGridPlot, title="Data")

except Exception as e:
    print(f"Error processing Tab 1 data: {e}")
    raise

# ============================
# TAB 2: Interactive Graphs
# ============================

try:
    print("Creating Interactive Graphs Tab...")

    # Aggregate total records by Month for Bar Chart (already done in SummaryDf)
    # Aggregate total Amount per Month for Line Chart
    AmountSummaryDf = BFIPublicDataDF.groupby('Month')['Amount'].sum().reset_index(name='Total Amount')

    # Merge both summaries for consistent x-axis
    GraphSummaryDf = pd.merge(SummaryDf, AmountSummaryDf, on='Month')
    print("GraphSummaryDf after merge:")
    print(GraphSummaryDf.head())

    # Check for NaN values
    print("\nChecking for NaN values in GraphSummaryDf:")
    print(GraphSummaryDf.isnull().sum())

    # Ensure 'Total Records' and 'Total Amount' are numeric
    print("\nData types in GraphSummaryDf:")
    print(GraphSummaryDf.dtypes)

    # Handle any potential NaN values or incorrect data types
    GraphSummaryDf['Total Records'] = pd.to_numeric(GraphSummaryDf['Total Records'], errors='coerce').fillna(0).astype(int)
    GraphSummaryDf['Total Amount'] = pd.to_numeric(GraphSummaryDf['Total Amount'], errors='coerce').fillna(0.0)
    print("\nAfter ensuring correct data types:")
    print(GraphSummaryDf[['Total Records', 'Total Amount']].head())

    # Convert 'Month' to datetime for sorting and plotting
    GraphSummaryDf['Month_Date'] = pd.to_datetime(GraphSummaryDf['Month'], format='%B %Y')
    GraphSummaryDf.sort_values('Month_Date', inplace=True)
    print("\nGraphSummaryDf after adding 'Month_Date' and sorting:")
    print(GraphSummaryDf.head())

    # Update the ColumnDataSource
    GraphSummarySource = ColumnDataSource(GraphSummaryDf)

    # Define x_range for bar_chart
    x_range = GraphSummaryDf['Month'].tolist()
    print("\nx_range for bar_chart:")
    print(x_range)

    # Create Bar Chart for Total Records per Month
    bar_chart = figure(
        x_range=x_range,
        height=600,
        width=1000,
        title="Total Records per Month",
        toolbar_location=None,
        tools=""
    )

    bar_chart.vbar(
        x='Month',
        top='Total Records',
        width=0.9,
        source=GraphSummarySource,
        legend_label="Total Records",
        color=SECONDARY_COLOR
    )

    # Add Hover Tool to Bar Chart
    hover_bar = HoverTool(tooltips=[
        ("Month", "@Month"),
        ("Total Records", "@{Total Records}")
    ], mode='vline')

    bar_chart.add_tools(hover_bar)

    # Style the Bar Chart
    bar_chart.xgrid.grid_line_color = None
    bar_chart.y_range.start = 0
    bar_chart.legend.orientation = "horizontal"
    bar_chart.legend.location = "top_center"
    bar_chart.axis.axis_label = "Month"
    bar_chart.axis.major_label_orientation = 1.0

    # Create Line Chart for Total Amount Over Time
    line_chart = figure(
        x_axis_type="datetime",
        height=600,
        width=1000,
        title="Total Amount Over Time",
        toolbar_location=None,
        tools=""
    )

    line_chart.line(
        x='Month_Date',
        y='Total Amount',
        source=GraphSummarySource,
        line_width=2,
        color=ACCENT_COLOR,
        legend_label="Total Amount"
    )

    # Add Circle Markers to Line Chart
    line_chart.circle(
        x='Month_Date',
        y='Total Amount',
        source=GraphSummarySource,
        size=6,
        color=ACCENT_COLOR
    )

    # Add Hover Tool to Line Chart
    hover_line = HoverTool(tooltips=[
        ("Month", "@Month"),
        ("Total Amount (£)", "@{Total Amount}{0.00 a}")
    ], mode='vline')

    line_chart.add_tools(hover_line)

    # Style the Line Chart
    line_chart.xaxis.axis_label = "Month"
    line_chart.yaxis.axis_label = "Total Amount (£)"
    line_chart.legend.location = "top_left"
    line_chart.legend.click_policy = "hide"
    line_chart.xaxis.major_label_orientation = 1.0

    # Arrange Graphs in a Column with Stretching
    graphs_layout = column(
        bar_chart,
        line_chart,
        sizing_mode='stretch_both'
    )

    # Create Div for Graphs Tab Header
    graphs_header_div = Div(
        text="<h2>Interactive Graphs</h2>",
        styles=header_div_style,
        width=1600
    )

    # Combine Header and Graphs
    graphs_tab_content = column(
        graphs_header_div,
        graphs_layout,
        sizing_mode='stretch_both'
    )

    # Define TabPanel for Tab 2
    tab2 = TabPanel(child=graphs_tab_content, title="Graphs")
    print("Interactive Graphs Tab created successfully.")

except Exception as e:
    print(f"Error creating Graphs tab: {e}")
    raise

# ============================
# Configure Tabs
# ============================

try:
    print("Configuring tabs...")
    # Tabs: tab0 (Summary), tab1 (Data), tab2 (Graphs)
    tabs = Tabs(tabs=[tab0, tab1, tab2])
    print("Tabs configured successfully.")
except Exception as e:
    print(f"Error configuring tabs: {e}")
    raise

# ============================
# Create and Display the Dashboard
# ============================

try:
    print("Rendering dashboard...")
    show(tabs, theme=custom_theme)
    print("Dashboard rendered successfully.")
except Exception as e:
    print(f"Error rendering dashboard: {e}")
    raise
