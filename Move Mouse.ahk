InputBox , Qtd, !!!Favor confirmar!!!, Por quantos minutos deseja mexer o Mouse?, , 320, 130

If ErrorLevel{
	MsgBox , Quantidade não Definida!!!
	ExitApp
}
Loop %Qtd%{
	Loop %Qtd%{
		Loop %Qtd%{
			Loop %Qtd%{
				Loop %Qtd%{
					Loop %Qtd%{
						Loop %Qtd%{
							Loop %Qtd%{
								Loop %Qtd%{
									Loop %Qtd%{
										Loop %Qtd%{
											Loop %Qtd%{
												Loop %Qtd%{
													Loop %Qtd%{
															Loop %Qtd%{

																Sleep , 5000
																MouseMove, 250, 250 ;[, Speed, R]
																Sleep , 5000
																MouseMove, 500, 500

															}
															Send , {DOWN}
													}
												}
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}
}
PAUSE::PAUSE