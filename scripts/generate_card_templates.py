def manual_template_capture(self):
    """Modo manual para capturar templates - VERSIÓN CORREGIDA"""
    print("\n" + "=" * 60)
    print("🎴 MODO MANUAL DE CAPTURA DE TEMPLATES")
    print("=" * 60)
    
    print("\n📋 CARTAS VÁLIDAS:")
    print("  Ranks: A, K, Q, J, 10, 9, 8, 7, 6, 5, 4, 3, 2")
    print("  Suits: s (♠), h (♥), d (♦), c (♣)")
    print("\n  Ejemplos: Ah, Ks, Qd, Jc, 10h, 9s, 8d, 7c")
    
    print("\nINSTRUCCIONES:")
    print("1. Abre GG Poker o PokerStars en una mesa")
    print("2. Asegúrate de que las cartas sean visibles")
    print("3. Para CADA carta:")
    print("   - Coloca el mouse SOBRE la carta")
    print("   - Presiona ESPACIO para capturar")
    print("   - Ingresa el valor (ej: Ah, Ks, Qd, Jc, 10h)")
    print("4. Presiona ESC para terminar")
    print("\nPresiona ESPACIO para comenzar...")
    
    keyboard.wait('space')
    
    templates_captured = 0
    captured_cards = []
    
    while True:
        print(f"\n📸 [{templates_captured}/52] Listo para capturar...")
        print("   Coloca el mouse SOBRE la carta y presiona ESPACIO")
        print("   Presiona ESC para terminar")
        
        try:
            # Esperar a que presionen espacio o ESC
            key = keyboard.read_key()
            
            if key == 'esc':
                print("\n⏹️  Captura interrumpida por el usuario")
                break
            
            if key != 'space':
                continue
            
            # Obtener posición del mouse
            mouse_x, mouse_y = pyautogui.position()
            logger.info(f"Posición del mouse: ({mouse_x}, {mouse_y})")
            
            # Capturar pantalla
            screenshot = self.capture_screen()
            if screenshot is None:
                print("❌ Error capturando pantalla")
                continue
            
            # Definir región alrededor del mouse
            card_w, card_h = self.config["card_size"]
            region_x = max(0, mouse_x - card_w // 2)
            region_y = max(0, mouse_y - card_h // 2)
            
            # Extraer la carta
            card_region = (region_x, region_y, card_w, card_h)
            card_img = self.extract_card_image(screenshot, card_region)
            
            if card_img is None:
                print("❌ No se pudo extraer la carta")
                continue
            
            # Mostrar preview
            cv2.imshow("Preview de la carta - Presiona una tecla para continuar", card_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
            # Preguntar por el nombre de la carta
            print("\n💬 ¿Qué carta es esta?")
            card_name = input("Ingresa RankSuit (ej: Ah, Ks, Qd, Jc, 10h): ").strip().upper()
            
            if len(card_name) >= 2:
                # Extraer rank y suit (manejar '10' que tiene 2 caracteres)
                if card_name.startswith('10') and len(card_name) >= 3:
                    rank = '10'
                    suit = card_name[2]
                else:
                    rank = card_name[0]
                    suit = card_name[1] if len(card_name) > 1 else ''
                
                # Lista completa de ranks válidos (incluye '10')
                valid_ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
                valid_suits = ['S', 'H', 'D', 'C']
                
                # Validar
                if rank.upper() in valid_ranks and suit.upper() in valid_suits:
                    # Formatear correctamente (rank mayúscula, suit minúscula)
                    formatted_rank = rank.upper()
                    formatted_suit = suit.lower()
                    final_card_name = f"{formatted_rank}{formatted_suit}"
                    
                    # Verificar si ya capturamos esta carta
                    if final_card_name in captured_cards:
                        print(f"⚠️  Ya capturaste {final_card_name}. ¿Sobrescribir? (s/n)")
                        overwrite = input().strip().lower()
                        if overwrite != 's':
                            print("⏭️  Saltando esta carta...")
                            continue
                    
                    # Guardar template
                    template_path = self.output_dir / f"{final_card_name}.png"
                    cv2.imwrite(str(template_path), card_img)
                    
                    templates_captured += 1
                    captured_cards.append(final_card_name)
                    
                    print(f"✅ Template guardado: {final_card_name}")
                    print(f"📍 Guardado en: {template_path}")
                    
                    # Mostrar estadísticas
                    remaining = 52 - templates_captured
                    progress = (templates_captured / 52) * 100
                    print(f"📊 Progreso: {templates_captured}/52 ({remaining} restantes) - {progress:.1f}%")
                    
                    # Mostrar próximas cartas recomendadas
                    if templates_captured < 10:
                        print("\n🎯 Próximas cartas recomendadas:")
                        recommended = ['Ah', 'Ks', 'Qd', 'Jc', '10h', '9s', '8d', '7c', '6h', '5s']
                        remaining_rec = [c for c in recommended if c not in captured_cards]
                        print(f"   {', '.join(remaining_rec[:5])}")
                    
                else:
                    print("❌ Nombre inválido.")
                    print(f"   Rank válidos: {', '.join(valid_ranks)}")
                    print(f"   Suit válidos: {', '.join(valid_suits)}")
                    print("   Ejemplo: 'Ah', 'Ks', 'Qd', 'Jc', '10h'")
            else:
                print("❌ Nombre demasiado corto. Ejemplo: 'Ah', 'Ks', '10h'")
                
        except keyboard.KeyboardInterrupt:
            print("\n⏹️  Captura interrumpida")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE CAPTURA")
    print("=" * 60)
    
    if captured_cards:
        print(f"✅ Templates capturados: {len(captured_cards)}")
        print(f"📁 Guardados en: {self.output_dir}")
        
        # Ordenar cartas capturadas
        captured_cards.sort()
        print("\n🃏 Cartas capturadas:")
        
        # Mostrar en grupos de 10
        for i in range(0, len(captured_cards), 10):
            group = captured_cards[i:i+10]
            print(f"   {', '.join(group)}")
    else:
        print("⚠️  No se capturaron templates")
    
    print(f"\n📈 Progreso total: {len(captured_cards)}/52 ({(len(captured_cards)/52)*100:.1f}%)")
    
    return len(captured_cards)