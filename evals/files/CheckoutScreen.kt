package com.example.booking.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun CheckoutScreen(onPay: () -> Unit) {
    var name by remember { mutableStateOf("") }
    var card by remember { mutableStateOf("") }
    var expiry by remember { mutableStateOf("") }
    var cvc by remember { mutableStateOf("") }
    var coupon by remember { mutableStateOf("") }
    var agree by remember { mutableStateOf(false) }

    Column(
        Modifier
            .fillMaxSize()
            .background(Brush.verticalGradient(listOf(Color(0xFF6A5AE0), Color(0xFF9C6BFF))))
            .padding(16.dp)
    ) {
        Text("Checkout", color = Color.White, fontSize = 28.sp, fontWeight = FontWeight.Bold)
        Spacer(Modifier.height(8.dp))
        Text("Cabin in the Dolomites · 3 nights", color = Color(0xFFDDD6FF), fontSize = 12.sp)
        Spacer(Modifier.height(24.dp))

        Card(shape = RoundedCornerShape(24.dp), colors = CardDefaults.cardColors(containerColor = Color.White.copy(alpha = 0.15f))) {
            Column(Modifier.padding(16.dp)) {
                OutlinedTextField(name, { name = it }, placeholder = { Text("Name") })
                OutlinedTextField(card, { card = it }, placeholder = { Text("Card number") })
                Row {
                    OutlinedTextField(expiry, { expiry = it }, placeholder = { Text("MM/YY") }, modifier = Modifier.weight(1f))
                    OutlinedTextField(cvc, { cvc = it }, placeholder = { Text("CVC") }, modifier = Modifier.weight(1f))
                }
                OutlinedTextField(coupon, { coupon = it }, placeholder = { Text("Coupon") })
            }
        }

        Spacer(Modifier.height(16.dp))
        Row(verticalAlignment = Alignment.CenterVertically) {
            Checkbox(agree, { agree = it }, modifier = Modifier.size(20.dp))
            Text("I agree to the terms", color = Color(0xFFCFC8FF), fontSize = 11.sp)
        }

        Spacer(Modifier.weight(1f))
        Text("Total €642", color = Color.White, fontSize = 14.sp)
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            TextButton(onClick = {}) { Text("Cancel", color = Color.White) }
            Button(onClick = onPay, shape = RoundedCornerShape(50)) { Text("Continue") }
        }
    }
}
